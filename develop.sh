#!/bin/bash
#
# Script to control Mastrms in dev and test
#

TOPDIR=$(cd `dirname $0`; pwd)
ACTION=$1
shift

# break on error
set -e

PORT='8000'

PROJECT_NAME='mastrms'
AWS_BUILD_INSTANCE='aws_rpmbuild_centos6'
AWS_STAGING_INSTANCE='aws_syd_mastrms_staging'
TARGET_DIR="/usr/local/src/${PROJECT_NAME}"
CLOSURE="/usr/local/closure/compiler.jar"
TESTING_MODULES="argparse dingus xvfbwrapper nose"
MODULES="MySQL-python==1.2.3 psycopg2==2.4.6 Werkzeug flake8 ${TESTING_MODULES}"
PIP_OPTS="-v -M --download-cache ~/.pip/cache --index-url=https://restricted.crate.io"

# A lot of tests need a database and/or X display to run. So the full
# test suite TEST_LIST and the tests which don't need a database or X
# are in NOSE_TEST_LIST, because they can be run outside the django
# test runner.
TEST_LIST="mastrms.repository.tests mastrms.mdatasync_client.client.test.tests mastrms.mdatasync_server.tests"
NOSE_TEST_LIST="mastrms.mdatasync_client.client.test.tests:DataSyncServerTests mastrms.mdatasync_client.client.test.tests:MSDataSyncAPITests mastrms.mdatasync_client.client.test.tests:MSDSImplTests"


settings() {
    export DJANGO_SETTINGS_MODULE="${PROJECT_NAME}.settings"
}

activate_virtualenv() {
    source ${TOPDIR}/virt_${PROJECT_NAME}/bin/activate
}

# ssh setup, make sure our ccg commands can run in an automated environment
KEYFILE="ccg-syd-staging.pem"
ci_ssh_agent() {
    ssh-add -l | grep $KEYFILE > /dev/null || ci_ssh_agent_start
}

ci_ssh_agent_start() {
    ssh-agent > /tmp/agent.env.sh
    source /tmp/agent.env.sh
    rm -f /tmp/agent.env.sh
    ssh-add ~/.ssh/$KEYFILE
    trap ci_ssh_agent_kill EXIT
}

ci_ssh_agent_kill() {
    if [ -n "${SSH_AGENT_PID}" ]; then
        ssh-agent -k > /tmp/agent.env.sh
        source /tmp/agent.env.sh
        rm -f /tmp/agent.env.sh
    fi
}

build_number_head() {
    export TZ=Australia/Perth
    DATE=`date`
    TIP=`hg tip --template "{node}" 2>/dev/null || /bin/true`
    echo "# Generated by develop.sh"
    echo "build.timestamp=\"$DATE\""
    echo "build.tip=\"$TIP\""
}

# build RPMs on a remote host from ci environment
ci_remote_build() {
    time ccg ${AWS_BUILD_INSTANCE} boot
    time ccg ${AWS_BUILD_INSTANCE} puppet
    time ccg ${AWS_BUILD_INSTANCE} shutdown:50

    cd ${TOPDIR}

    if [ -z "$BAMBOO_BUILDKEY" ]; then
        # We aren't running under Bamboo, create new build-number.txt.
        build_number_head > build-number.txt
    else
        # Bamboo has already put some useful information in
        # build-number.txt, so append to it.
        build_number_head >> build-number.txt
    fi

    EXCLUDES="('bootstrap'\, '.hg*'\, '.git'\, 'virt*'\, '*.log'\, '*.rpm'\, 'mastrms/build'\, 'mastrms/dist'\, '*.egg-info'\, 'mastrms/mastrms/mdatasync_client/supportwin32')"
    SSH_OPTS="-o StrictHostKeyChecking\=no"
    RSYNC_OPTS="-l"
    time ccg ${AWS_BUILD_INSTANCE} rsync_project:local_dir=./,remote_dir=${TARGET_DIR}/,ssh_opts="${SSH_OPTS}",extra_opts="${RSYNC_OPTS}",exclude="${EXCLUDES}",delete=True
    time ccg ${AWS_BUILD_INSTANCE} build_rpm:centos/${PROJECT_NAME}.spec,src=${TARGET_DIR}

    mkdir -p build
    ccg ${AWS_BUILD_INSTANCE} getfile:rpmbuild/RPMS/x86_64/${PROJECT_NAME}*.rpm,build/
}

# publish rpms to testing repo
ci_rpm_publish() {
    time ccg publish_testing_rpm:build/${PROJECT_NAME}*.rpm,release=6
}

# copy a version from testing repo to release repo
rpm_release() {
    if [ -z "$1" ]; then
        echo "rpm_release requires an rpm filename argument"
        usage
        exit 1
    fi

    time ccg release_rpm:$1,release=6
}

# destroy our ci build server
ci_remote_destroy() {
    ccg ${AWS_BUILD_INSTANCE} destroy
}


# puppet up staging which will install the latest rpm
ci_staging() {
    ccg ${AWS_STAGING_INSTANCE} boot
    ccg ${AWS_STAGING_INSTANCE} puppet
    ccg ${AWS_STAGING_INSTANCE} shutdown:50
}

# run tests on staging
ci_staging_tests() {
    # /tmp is used for test results because the apache user has
    # permission to write there.
    REMOTE_TEST_DIR=/tmp
    REMOTE_TEST_RESULTS=${REMOTE_TEST_DIR}/tests.xml

    # Grant permission to create a test database. Assume that database
    # user is same as project name for now.
    DATABASE_USER=${PROJECT_NAME}
    ccg ${AWS_STAGING_INSTANCE} dsudo:"su postgres -c \"psql -c 'ALTER ROLE ${DATABASE_USER} CREATEDB;'\""

    # fixme: this config should be put in nose.cfg or settings.py or similar
    EXCLUDES="--exclude\=yaphc --exclude\=esky --exclude\=httplib2"

    # Start virtual X server here to work around a problem starting it
    # from xvfbwrapper.
    ccg ${AWS_STAGING_INSTANCE} drunbg:"Xvfb \:0"

    sleep 2

    # firefox won't run without a profile directory, dbus and gconf
    # also need to write in home directory.
    ccg ${AWS_STAGING_INSTANCE} dsudo:"chown apache:apache /var/www"

    # Run tests, collect results
    ccg ${AWS_STAGING_INSTANCE} dsudo:"cd ${REMOTE_TEST_DIR} && env DISPLAY\=\:0 dbus-launch timeout -sHUP 30m ${PROJECT_NAME} test --verbosity\=2 --liveserver\=localhost\:8082\,8090-8100\,9000-9200\,7041 --noinput --with-xunit --xunit-file\=${REMOTE_TEST_RESULTS} ${TEST_LIST} ${EXCLUDES} || true"
    ccg ${AWS_STAGING_INSTANCE} getfile:${REMOTE_TEST_RESULTS},./
}


# lint using flake8
lint() {
    activate_virtualenv
    cd ${TOPDIR}
    flake8 ${PROJECT_NAME} --ignore=E501 --count
}


# lint js, assumes closure compiler
jslint() {
    JSFILES="${TOPDIR}/mastrms/mastrms/app/static/js/*.js ${TOPDIR}/mastrms/mastrms/app/static/js/repo/*.js"
    for JS in $JSFILES
    do
        java -jar ${CLOSURE} --js $JS --js_output_file output.js --warning_level DEFAULT --summary_detail_level 3
    done
}


# run the tests using django-admin.py
djangotests() {
    TEST_EXCLUDES="--exclude=yaphc --exclude=esky --exclude=httplib2"
    LIVESERVER="--liveserver=localhost:8082,8090-8100,9000-9200,7041"

    activate_virtualenv
    dbus-launch django-admin.py test --noinput ${LIVESERVER} \
        --with-xunit --xunit-file="${TARGET_DIR}/tests.xml" \
        ${TEST_EXCLUDES} ${TEST_LIST} || true
}


nose_tests() {
    activate_virtualenv
    export PYTHONPATH="${TARGET_DIR}:${PYTHONPATH}"
    nosetests --with-xunit --xunit-file="${TARGET_DIR}/tests.xml" \
        -v -w ${TARGET_DIR} ${NOSE_TEST_LIST} || true
}


nose_collect() {
    activate_virtualenv
    nosetests -v -w tests --collect-only
}


dropdb() {
    echo "todo"
}


installapp() {
    # check requirements
    which virtualenv >/dev/null

    echo "Install ${PROJECT_NAME}"
    virtualenv --system-site-packages ${TOPDIR}/virt_${PROJECT_NAME}
    pushd ${TOPDIR}/${PROJECT_NAME}
    ../virt_${PROJECT_NAME}/bin/pip install ${PIP_OPTS} -e .
    popd
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/pip install ${PIP_OPTS} ${MODULES}
}


# django syncdb, migrate and collect static
syncmigrate() {
    echo "syncdb"
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/django-admin.py syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> syncdb-develop.log
    echo "migrate"
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/django-admin.py migrate --settings=${DJANGO_SETTINGS_MODULE} 1> migrate-develop.log
    echo "collectstatic"
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> collectstatic-develop.log
}

ipaddress() {
    if [ -n "$1" ]; then
        DEV="dev $1"
    else
        DEV=""
    fi
    ip -4 addr show ${DEV} 2> /dev/null | awk '/inet / { gsub(/\/.*/, ""); print $2; }'
}

# start runserver
startserver() {
    echo "Visit http://$(ipaddress eth0):${PORT}/"
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/django-admin.py runserver_plus 0.0.0.0:${PORT}
}


pythonversion() {
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/python -V
}


pipfreeze() {
    echo "${PROJECT_NAME} pip freeze"
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/pip freeze
    echo '' 
}


clean() {
    find ${TOPDIR}/${PROJECT_NAME} -name "*.pyc" -exec rm -rf {} \;
}


purge() {
    rm -rf ${TOPDIR}/virt_${PROJECT_NAME}
    rm *.log
}


usage() {
    echo ""
    echo "Usage ./develop.sh (test|nosetests|lint|jslint|dropdb|start|install|clean|purge|pipfreeze|pythonversion|ci_remote_build|ci_staging|ci_staging_tests|ci_rpm_publish|rpm_release VERSION|ci_remote_destroy)"
    echo ""
}

case ${ACTION} in
pythonversion)
    pythonversion
    ;;
pipfreeze)
    pipfreeze
    ;;
test)
    settings
    djangotests
    ;;
nosetests)
    settings
    nose_tests
    ;;
lint)
    lint
    ;;
jslint)
    jslint
    ;;
syncmigrate)
    settings
    syncmigrate
    ;;
start)
    settings
    startserver
    ;;
install)
    settings
    installapp
    ;;
ci_remote_build)
    ci_ssh_agent
    ci_remote_build
    ;;
ci_remote_destroy)
    ci_ssh_agent
    ci_remote_destroy
    ;;
ci_rpm_publish)
    ci_ssh_agent
    ci_rpm_publish
    ;;
rpm_release)
    ci_ssh_agent
    rpm_release $*
    ;;
ci_staging)
    ci_ssh_agent
    ci_staging
    ;;
ci_staging_tests)
    ci_ssh_agent
    ci_staging_tests
    ;;
dropdb)
    dropdb
    ;;
clean)
    settings
    clean
    ;;
purge)
    settings
    clean
    purge
    ;;
*)
    usage
esac

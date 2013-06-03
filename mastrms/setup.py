import setuptools
import os
from setuptools import setup

data_files = {}
start_dir = os.getcwd()
for package in ('app', 'admin', 'dashboard', 'login', 'mdatasync_server', 'quote', 'registration', 'repository', 'users'):
    data_files['mastrms.' + package] = []
    os.chdir(os.path.join('mastrms', package))
    for data_dir in ('templates', 'static', 'migrations', 'fixtures', 'views', 'utils'):
        data_files['mastrms.' + package].extend(
            [os.path.join(subdir,f) for (subdir, dirs, files) in os.walk(data_dir) for f in files])
    os.chdir(start_dir)

setup(name='django-mastrms',
    version='1.2.2',
    description='Mastr MS',
    long_description='Django Mastr MS web application',
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    packages=[
        'mastrms',
        'mastrms.app',
        'mastrms.admin',
        'mastrms.dashboard',
        'mastrms.login',
        'mastrms.mdatasync_client',
        'mastrms.mdatasync_server',
        'mastrms.quote',
        'mastrms.registration',
        'mastrms.repository',
        'mastrms.users'
    ],
    package_data=data_files,
    zip_safe=False,
    install_requires=[
        'Django==1.4.5',
        'South==0.7.3',
        'ccg-extras==0.1.5',
        'ccg-auth==0.3.2',
        'django-picklefield==0.1.9',
        'django-templatetag-sugar==0.1',
        'pyparsing==1.5.6',
        'wsgiref==0.1.2',
        'python-memcached==1.44',
        'django-extensions>=0.7.1',
        'python-ldap==2.3.13',
        'django-userlog==0.1',
    ],
    dependency_links = [
        "http://repo.ccgapps.com.au"
    ],
)
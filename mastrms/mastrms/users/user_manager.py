from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import Group

import logging

# This class has been created when dependency on LDAP has been removed from application
# The idea is to support the methods LDAPHandler was supporting and return data in the exact same format
# as it was from LDAP (but now from the DB) to minimize the rewriting that has to be done

logger = logging.getLogger('mastrms.general')

def get_user_manager():
    return DBUserManager()

class DBUserManager(object):
    def get_user_details(self, username):
        if not username or username == "nulluser":
            logger.warning("Looked up details for the nulluser")
            return {}

        from mastrms.users.models import User
        try:
            django_user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.exception("User \"%s\" doesn't exist" % username)
            return {}

        details_dict = django_user.to_dict()

        details_dict['groups'] = [g.name for g in Group.objects.filter(user=django_user)]

        return details_dict

    def list_groups(self):
        return [g.name for g in Group.objects.all()]

    def add_group(self, groupname):
        try:
            groupname = groupname.strip()
            Group.objects.create(name=groupname)
        except Exception, e:
            logger.exception("Couldn't create group %s." % groupname)
            return False
        return True

    def rename_group(self, oldname, newname):
        try:
            oldname = oldname.strip()
            newname = newname.strip()
            group = Group.objects.get(name=oldname)
            group.name = newname
            group.save()
        except Exception, e:
            logger.exception("Couldn't rename group %s to group %s." % (oldname, newname))
            return False
        return True

    def delete_group(self, groupname):
        try:
            group = Group.objects.get(name=groupname)
            group.delete()
        except Exception, e:
            logger.exception("Couldn't delete group %s." % groupname)
            return False
        return True

    def get_user_groups(self, username):
        return [g.name for g in Group.objects.filter(user__username=username)]

    def list_users(self, searchGroup, method= 'and'):
        from mastrms.users.models import User
        users_qs = User.objects.all()
        if searchGroup:
            users_qs = User.objects
            filter_cond = None
            for g in searchGroup:
                if method == 'and':
                    users_qs = users_qs.filter(groups__name=g)
                else:
                    if filter_cond is None:
                        filter_cond = Q(groups__name=g)
                    else:
                        filter_cond = filter_cond | Q(groups__name=g)
            if method != 'and':
                users_qs = User.objects.filter(filter_cond)

        return [u.to_dict() for u in users_qs]


    def update_staff_status(self, user):
        #if the user belongs to more than one Group, they should be
        #django staff.  Else, they shouldnt.
        from mastrms.users.models import getMadasUser
        mauser = getMadasUser(user.username)
        if not mauser.IsClient:
            user.is_staff=True
            user.save()
        else:
            user.is_staff=False
            user.save()

    def add_user(self, username, detailsDict):
        from mastrms.users.models import User
        username = username.strip()
        if User.objects.filter(username=username).exists():
            logger.warning('A user called %s already existed. Refusing to add.' % username)
            return None
        django_user = User.objects.create(username=username)
        django_user.set_from_dict(detailsDict)
        django_user.save()
        return django_user

    def update_user(self, user, newusername, newpassword, detailsDict):
        from mastrms.users.models import User

        if newusername is None:
            newusername = user.username
        elif newusername != user.username:
            if User.objects.filter(username=newusername).exists():
                logger.warning('New Username %s already existed.' % newusername)
            else:
                user.username = newusername

        if newpassword:
            user.set_password(newpassword)
            user.passwordResetKey = ""

        user.set_from_dict(detailsDict)

        user.save()

        return True

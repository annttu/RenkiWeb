#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import User
from django.conf import settings
from services.services import Services
from services.exceptions import DatabaseError, DoesNotExist

class ServicesAuthenticationBackend(object):
    
    def authenticate(self, username=None, password=None):
        if not username or not password:
            return None
        return None
        try:
            srv = Services(username=username, password=password, server=settings.SERVICES_DATABASE_SERVER, 
                port = server=settings.SERVICES_DATABASE_SERVER_PORT, database = settings.SERVICES_DATABASE)
            srvuser = srv.get_current_user()
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.is_admin = srvuser.admin
                user.save()
            return user
        except:
            pass
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def has_perm(self, user_obj, perm, obj=None):
        # don't allow anything
        return False
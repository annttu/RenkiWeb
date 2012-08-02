#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import User
from django.conf import settings
from services.services import Services
from services.exceptions import DatabaseError, DoesNotExist
from django.contrib.auth.backends import ModelBackend

class ServicesAuthenticationBackend(ModelBackend):
    
    def authenticate(self, username=None, password=None):
        """Authenticate user aganist Services database"""
        if not username or not password:
            return None
        try:
            if srv:
                print('Srv object already')
        except:
            pass
        try:
            srv = Services(username=username, password=password, server=settings.SERVICES_DATABASE_SERVER, 
                port = settings.SERVICES_DATABASE_SERVER_PORT, database = settings.SERVICES_DATABASE,
                verbose=False, dynamic_load=False)
            srv.login()
            print('SUCCESS')
        except RuntimeError as e:
            return None
        try:
            srv.username = username
            srvuser = srv.get_current_user()
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.is_admin = srvuser.admin
                user.save()
            user.srv = srv
            del srv
            del srvuser
            return user
        except RuntimeError as e:
            print("ERROR: %s" % e)
            pass
        return None

    def get_user(self,user_id, **kwargs):
        try:
            return User.objects.get(id=user_id)
        except:
            return None

#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.core.cache import get_cache
from uuid import uuid4
from django.shortcuts import redirect

class ServicesMiddleware(object):
    
    def set_srv(self, request, data):
        cache = get_cache('inprocess')
        key = str(uuid4())
        cache.set(key, data)
        request.session['srv'] = key
        # Set expire time to 1h
        request.session.set_expiry(3600)
        request.session.save()
        return data

    def process_request(self, request):
        """Redirect to login page if no 
        valid services instance found"""
        cache = get_cache('inprocess')
        if 'srv' in request.session:
            key = request.session['srv']
            if cache.get(key):
                return
        #prevent redirect loop
        if request.META['PATH_INFO'] not in ['/logout','/login']:
            return redirect('/login?next=%s' % request.META['PATH_INFO'])

    #def process_request(self, request):
    #    try:
    #        request.srv = self.get_srv(request)
    #        print('success to get session')
    #    except:
    #        pass
    #    return None

    #def process_response(self, request, response):
    #    print(response.status_code)
    #    return response
    def process_response(self, request, response):
        try:
            self.set_srv(request, request.srv)
            print('Success to save session')
        except Exception as e:
            print('Failed to save session %s' % e)
        return response

    #def process_exception(self, request, exception):
    #    return
    #    try:
    #        session = request.db_session
    #    except AttributeError:
    #        return
    #    session.rollback()
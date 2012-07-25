#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings

class MySQLAlchemySessionMiddleware(object):
    def process_request(self, request):
        # this need modification
        if request.session.get('services_connection', None):
            request.db_session = request.session['services_connection'].Session()
        else:
            request.db_session = None
        return request

    def process_response(self, request, response):
        try:
            session = request.db_session
        except AttributeError:
            return response
        try:
            session.commit()
            return response
        except:
            session.rollback()
            raise

    def process_exception(self, request, exception):
        try:
            session = request.db_session
        except AttributeError:
            return
        session.rollback()
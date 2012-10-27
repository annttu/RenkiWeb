#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
from django.core.cache import get_cache
from django.contrib import messages

from renki.forms import DomainForm, PortForm

from services.services import Services
from services.exceptions import DoesNotExist

import logging
logging = logging.getLogger('renki')

    
def get_srv(request):
    cache = get_cache('inprocess')
    if 'srv' in request.session:
        key = request.session['srv']
        data = cache.get(key)
        return data
    return None

@login_required
def index(request, **kwargs):
    messages = []
    if 'messages' in kwargs:
        messages = kwargs['messages']
    return render_to_response('renki/index.html',{'messages': messages},
        context_instance=RequestContext(request))
        
def my_login(request, next=None, **kwargs):
    errormsg = ''
    try:
        if request.META['QUERY_STRING'].startswith('next='):
            next = request.META['QUERY_STRING'][5:]
    except:
        pass
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            # delete old session infomation
            my_logout(request)
            # login to services database
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # request.srv is used by ServicesMiddleware
                request.srv = user.srv
                if next:
                    return redirect(next)
                else:
                    kwargs = {'messages': [_('Successfully logged in!')]}
                    return redirect('success')
            else:
                errormsg = _('Invalid login')
    return render_to_response('renki/login.html',{'errormsg' : errormsg, 'next': next},
        context_instance=RequestContext(request))

@login_required
def success(request, **kwargs):
    srv = get_srv(request)
    if srv:
        username = srv.username
        message = 'Login successfully'
    else:
        username = 'Nobody'
        message = 'Login failed'
    return render_to_response('renki/index.html',{'message' : message, 'username' : username},
        context_instance=RequestContext(request))
        
def my_logout(request, **kwargs):
    try:
        cache = get_cache('inprocess')
        cache.delete(request.session['srv'])
        del request.session['srv']
    except:
        pass
    logout(request)
    return redirect('/login')
    
@login_required
def domains(request, **kwargs):
    try:
        srv = get_srv(request)
        domains = srv.domains.list()
    except Exception as e:
        logging.exception(e)
        domains = None
    return render_to_response('renki/domains.html',{'domains':domains},
        context_instance=RequestContext(request))

@login_required
def domains_edit(request, domain_id, **kwargs):
    messages = []
    try:
        srv = get_srv(request)
        domain = srv.domains.get(domain_id=domain_id)
    except Exception as e:
        logging.exception(e)
        raise Http404
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            domain.dns = form.cleaned_data['dns']
            domain.shared = form.cleaned_data['shared']
            domain.refresh_time = form.cleaned_data['refresh_time']
            domain.retry_time = form.cleaned_data['retry_time']
            domain.expire_time = form.cleaned_data['expire_time']
            domain.minimum_cache_time = form.cleaned_data['minimum_cache_time']
            domain.ttl = form.cleaned_data['ttl']
            domain.domain_type = form.cleaned_data['domain_type']
            domain.allow_transfer = []
            for a in form.cleaned_data['allow_transfer'].strip(',').split(','):
                domain.allow_transfer.append(a)
            domain.masters = []
            for m in form.cleaned_data['masters'].strip(',').split(','):
                domain.masters.append(m)
            srv.session.add(domain)
            try:
                srv.session.commit()
                messages.append(_('Succeed to save data'))
            except Exception as e:
                srv.log.exception(e)
                messages.append(_('Failed to save data'))
        else:
            messages.append(_('Form contain errors'))
    else:
        masters = ''
        for m in domain.masters:
            masters += '%s,' % m
        masters = masters.strip(',')
        allow_transfer = ''
        for m in domain.allow_transfer:
            allow_transfer += '%s,' % m
        allow_transfer = allow_transfer.strip(',')
        form = DomainForm(initial = {'shared':domain.shared, 'dns': domain.dns, 'refresh_time' : domain.refresh_time,
            'retry_time': domain.retry_time, 'expire_time': domain.expire_time,
            'minimum_cache_time': domain.minimum_cache_time, 'ttl':domain.ttl,
            'domain_type':domain.domain_type, 'masters': masters, 'allow_transfer': allow_transfer})
        form.fields['shared'].initial = domain.shared
        form.fields['dns'].initial = domain.dns
        print("FORM: %s" % vars(form.fields['dns']))
        form.fields['minimum_cache_time'].initial = domain.minimum_cache_time
    return render_to_response('renki/domains_edit.html',{'domain':domain, 'form':form, 'messages': messages},
        context_instance=RequestContext(request))



@login_required
def vhosts_edit(request, vhost_id, **kwargs):
    try:
        srv = get_srv(request)
        vhost = srv.vhosts.get(vhost_id=vhost_id)
    except Exception as e:
        logging.exception(e)
        raise Http404
    if request.method == 'POST':
        ## Do something magic here :)
        pass
    return render_to_response('renki/vhosts_edit.html',{'vhost':vhost},
        context_instance=RequestContext(request))

def ports(request, **kwargs):
    class Port:
        def __init__(self, name):
            self.ports = []
            self.name = name

    try:
        srv = get_srv(request)
        all_servers = srv.user_ports.list_servers()
    except Exception as e:
        logging.exception(e)
        raise Http404

    all_servers = [(server.server, server.server) for server in all_servers]

    if request.method == 'POST':
        form = PortForm(request.POST)
        form.fields['server'].choices = all_servers
        if form.is_valid():
            try:
                srv.user_ports.add(form.cleaned_data['server'],form.cleaned_data['info'])
                messages.info(request,_('Successfully added port'))
                form = PortForm()
                form.fields['server'].choices = all_servers
            except Exception as e:
                logging.exception(e)
                messages.error(request, _('Cannot add port'))
        else:
            messages.error(request, _('Form contains errors'))
    else:
        form = PortForm()
        form.fields['server'].choices = all_servers
    ports = srv.user_ports.list()
    servers = {}
    for port in ports:
        if port.server not in servers:
            servers[port.server] = Port(port.server)
        servers[port.server].ports.append(port)
    servers = [servers[server] for server in servers]
    return render_to_response('renki/ports.html', {'servers': servers, 'form': form},
                              context_instance=RequestContext(request))


@login_required
def databases(request, **kwargs):
    srv = get_srv(request)
    mysql = srv.mysql.list()
    psql  = srv.postgresql.list()
    return render_to_response('renki/databases.html', {'mysql':mysql,'postgresql':psql},
        context_instance=RequestContext(request))

def databases_passwd(request, database_id, **kwargs):
    srv = get_srv(request)
    try:
        db = srv.mysql.get_by_id(database_id)
    except DoesNotExist:
        try:
            db = srv.postgresql.get_by_id(database_id)
        except DoesNotExist:
            raise Http404
    if request.method == 'POST':
        return render_to_response('renki/database_passwd.html', {'messages': [_('Password changed!'), 'fake'], 'db': db},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('renki/database_passwd.html', {'db':db},
                                  context_instance=RequestContext(request))
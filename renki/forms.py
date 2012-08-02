#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from services.libs.tools import valid_ipv4_address, valid_ipv6_address

def IPlistValidator(value):
    iplist = value.strip(',')
    iplist = iplist.split(',')
    for ip in iplist:
        if valid_ipv4_address(ip):
            continue
        if valid_ipv6_address(ip):
            continue
        raise ValidationError(_('Invalid IP-address %s' % ip))
    return True

class DomainForm(forms.Form):
    shared = forms.BooleanField(required=False, initial=False)
    dns = forms.BooleanField(required=False, initial=True)
    refresh_time = forms.IntegerField(min_value=1,max_value=9999999, initial=28800)
    retry_time = forms.IntegerField(min_value=1,max_value=9999999, initial=7200)
    expire_time = forms.IntegerField(min_value=1,max_value=9999999, initial=1209600)
    minimum_cache_time = forms.IntegerField(min_value=1,max_value=9999999, initial=21600)
    ttl = forms.IntegerField(min_value=1,max_value=9999999, initial=10800)
    domain_type = forms.ChoiceField(choices=(('MASTER','master'),('SLAVE','slave'),('NONE','none')))
    masters = forms.CharField(required=False, validators=[IPlistValidator])
    masters.widget.attrs={'placeholder':_('IP-address')}
    allow_transfer = forms.CharField(required=False, validators=[IPlistValidator])
    allow_transfer.widget.attrs={'placeholder':_('IP-address')}

class NewDomainForm(DomainForm):
    name = forms.SlugField(required=True)
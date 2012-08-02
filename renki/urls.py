from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'renki.views.index', name='index'),
    url(r'^login/?$', 'renki.views.my_login', name='login'),
    url(r'^logout/?$', 'renki.views.my_logout', name='logout'),
    url(r'^success/?$', 'renki.views.success', name='success'),
    url(r'^domains/?$', 'renki.views.domains', name='domains'),
    url(r'^domains/(\d+)$', 'renki.views.domains_edit', name='domains_edit'),
    url(r'^vhosts/(\d+)$', 'renki.views.vhosts_edit', name='vhosts_edit'),
    url(r'^databases/(\d+)$', 'renki.views.databases_passwd', name='databases_passwd'),
    url(r'^databases/?$', 'renki.views.databases', name='databases'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

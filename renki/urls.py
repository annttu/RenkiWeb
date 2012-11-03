from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'renki.views.index', name='index'),
    url(r'^login/?$', 'renki.views.my_login', name='login'),
    url(r'^logout/?$', 'renki.views.my_logout', name='logout'),
    url(r'^domains/?$', 'renki.views.domains', name='domains'),
    url(r'^domains/(\d+)$', 'renki.views.domain_index', name='domain_index'),
    url(r'^domains/edit/(\d+)$', 'renki.views.domain_edit', name='domain_edit'),
    url(r'^vhosts/(\d+)$', 'renki.views.vhosts_edit', name='vhosts_edit'),
    url(r'^databases/add/(mysql|postgresql)$', 'renki.views.database_add', name='database_add'),
    url(r'^databases/(\d+)$', 'renki.views.databases_passwd', name='databases_passwd'),
    url(r'^databases/?$', 'renki.views.databases', name='databases'),
    url(r'^ports/?$', 'renki.views.ports', name='ports'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

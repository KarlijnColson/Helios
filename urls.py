# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    
    (r'^helios_auth/', include('helios_auth.urls')),
    (r'^helios/', include('helios.urls')),

    # SHOULD BE REPLACED BY APACHE STATIC PATH
    (r'booth/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/helios_booth'}),
    (r'verifier/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/helios_verifier'}),

    (r'static/helios_auth/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/helios_auth/media'}),
    (r'static/helios/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/helios/media'}),
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/server_ui/media'}),

    (r'^', include('server_ui.urls')),
    (r'^bulletin_board/', include('bulletin_board.urls')),
)

urlpatterns += i18n_patterns('',
    (r'^helios/', include('helios.urls')),
    (r'booth/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/helios_booth'}),
    
)

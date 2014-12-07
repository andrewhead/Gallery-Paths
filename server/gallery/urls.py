# encoding: utf-8

from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
from gallery.api import SightingResource
from gallery import views
from django.conf import settings
from django.conf.urls.static import static


sightingResource = SightingResource()

urlpatterns = patterns('',
    url(r'^index$', views.index),
    url(r'^$', views.index),
    url(r'^analytics$', views.analytics),
    url(r'^exhibitions$', views.exhibitions),
    url(r'^exhibits$', views.exhibits),
    url(r'^events$', views.events),
    url(r'^api/', include(sightingResource.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

''' Serve media files via Django if we are in DEBUG mode. '''
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

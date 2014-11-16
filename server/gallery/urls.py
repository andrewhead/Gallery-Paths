# encoding: utf-8

from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
from gallery.api import SightingResource
from gallery import views


sightingResource = SightingResource()

urlpatterns = patterns('',
    url(r'^api/', include(sightingResource.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home$', views.home),
    url(r'^paths$', views.paths),
    url(r'^$', views.home),
)

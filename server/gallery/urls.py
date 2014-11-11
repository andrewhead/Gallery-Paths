from django.conf.urls import patterns, include, url
from django.contrib import admin
from gallery.api import SightingResource


sightingResource = SightingResource()

urlpatterns = patterns('',
    url(r'^api/', include(sightingResource.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

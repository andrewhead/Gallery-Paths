#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from tastypie.resources import ModelResource
from gallery.models import Sighting
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization


class SightingResource(ModelResource):
    class Meta:
        queryset = Sighting.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ['post']

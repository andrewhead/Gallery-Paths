# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.core import serializers
import json

from models import Sighting


def index(request):
    context = {}
    return render(request, 'gallery/index.html')


def analytics(request):
    context = {}
    return render(request, 'gallery/analytics.html', context)


def events(request):
    recentSightings = reversed(Sighting.objects.order_by('-id')[:100])
    data = json.loads(serializers.serialize("json", recentSightings))
    contextInstance = RequestContext(request, {
        'data': data,
        'fields': Sighting._meta.fields,
    })
    return TemplateResponse(request, 'gallery/events.html', contextInstance)

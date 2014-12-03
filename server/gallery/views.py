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

    def flatten(d):
        def items():
            for key, value in d.items():
                if isinstance(value, dict):
                    for subkey, subvalue in flatten_dict(value).items():
                        yield subkey, subvalue
                else:
                    yield key, value
        return dict(items())

    recentSightings = reversed(Sighting.objects.order_by('-id')[:100])
    data = json.loads(serializers.serialize("json", recentSightings))
    flattenedData = []

    for d in data:
        d[Sighting._meta.pk.name] = d.pop('pk')
        flattenedData.append(flatten_dict(d))

    contextInstance = RequestContext(request, {
        'data': flattenedData,
        'fields': Sighting._meta.fields,
    })
    return TemplateResponse(request, 'gallery/events.html', contextInstance)

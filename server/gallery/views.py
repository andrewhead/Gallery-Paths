# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.core import serializers
from django.db import connection
import json
import jsonpickle

from models import Sighting


def index(request):
    context = {}
    return render(request, 'gallery/index.html')


def analytics(request):

    ''' Count dwellings per exhibit. '''
    cursor = connection.cursor()
    cursor.execute("SET @last='';")
    cursor.execute("""
        SELECT last_location, COUNT(last_location) FROM (
            SELECT id,@last AS last_location,@last:=location_id AS this_location 
            FROM gallery_sighting 
            HAVING last_location != this_location) 
        AS sub GROUP BY last_location;
    """)
    dwellCounts = dict([(str(i[0]), int(i[1])) for i in cursor.fetchall()])
    print dwellCounts
    cursor.close()

    ''' Get all sightings for map. '''
    sightings = list(Sighting.objects.all().values('visitor_id', 'location_id', 'time'))
    for s in sightings:
        s['visitor'] = s.pop('visitor_id')
        s['location'] = s.pop('location_id')
        s['tripIndex'] = 1

    context = {
        'dwellings': dwellCounts,
        'sightings': jsonpickle.encode(sightings, unpicklable=False),
    }
    return render(request, 'gallery/analytics.html', context)


def events(request):

    def flatten(d):
        def items():
            for key, value in d.items():
                if isinstance(value, dict):
                    for subkey, subvalue in flatten(value).items():
                        yield subkey, subvalue
                else:
                    yield key, value
        return dict(items())

    recentSightings = reversed(Sighting.objects.order_by('-id')[:100])
    data = json.loads(serializers.serialize("json", recentSightings))
    flattenedData = []

    for d in data:
        d[Sighting._meta.pk.name] = d.pop('pk')
        flattenedData.append(flatten(d))

    contextInstance = RequestContext(request, {
        'data': flattenedData,
        'fields': Sighting._meta.fields,
    })
    return TemplateResponse(request, 'gallery/events.html', contextInstance)

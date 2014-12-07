# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
import json
import jsonpickle
import datetime

from forms import ExhibitionForm, ExhibitForm
from models import Sighting, Exhibition, Exhibit


def index(request):
    context = {}
    return render(request, 'gallery/index.html')


@login_required
def exhibits(request):

    def _getExhibitForms(exhibition, post=False, withFiles=False):
        forms = []
        ids = [e.id for e in Exhibit.objects.filter(exhibition=exhibition)]
        for eid in ids:
            args = []
            kwargs = {}
            if post:
                args.append(request.POST)
            if withFiles:
                args.append(request.FILES)
            f = ExhibitForm(*args, prefix=str(eid), instance=Exhibit.objects.get(pk=eid))
            forms.append(f)
        return forms

    if request.method == "POST":
        exhibition = Exhibition.objects.get(pk=request.POST.get('e', -1))
        newForm = ExhibitForm(request.POST, request.FILES, prefix='new')
        formsToSave = []

        if request.POST.get("action") == "update":
            updateForms = _getExhibitForms(exhibition, post=True, withFiles=True)
            formsToSave.extend(updateForms)
        elif request.POST.get("action") == "add":
            updateForms = _getExhibitForms(exhibition)
            formsToSave.append(newForm)

        if all([f.is_valid() for f in formsToSave]):
            for f in formsToSave:
                f.save()
            return HttpResponseRedirect('exhibits?e=' + str(exhibition.pk))
        else:
            return render_to_response("gallery/exhibits.html", {
                "newForm": newForm,
                "forms": updateForms,
                "exhibition": exhibition,
            }, context_instance=RequestContext(request))

    if request.method == "GET":
        exhibition = Exhibition.objects.get(pk=request.GET.get('e', -1))
        updateForms = _getExhibitForms(exhibition)
        newForm = ExhibitForm(prefix='new', initial={'exhibition': exhibition})
        context = {
            'forms': updateForms,
            'newForm': newForm,
            'exhibition': exhibition,
        }
        return render(request, 'gallery/exhibits.html', context)


@login_required
def exhibitions(request):

    exhibitions = Exhibition.objects.all()

    if request.method == 'POST':
        if request.POST.get('action') == 'open':
            form = ExhibitionForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('exhibitions')
            else:
                return render_to_response("gallery/exhibitions.html", {
                    "newForm": newForm,
                    "exhibitions": exhibitions,
                }, context_instance=RequestContext(request))
        elif request.POST.get('action') == 'close':
            exhibition = Exhibition.objects.get(pk=request.POST.get('exhibition'))
            today = datetime.datetime.utcnow().date()
            exhibition.end = today
            exhibition.save()
            return HttpResponseRedirect('exhibitions')

    if request.method == 'GET':
        newForm = ExhibitionForm(initial={'name': "Exhibition Name"})
        context = {
            'newForm': newForm,
            'exhibitions': Exhibition.objects.all(),
        }
        return render(request, 'gallery/exhibitions.html', context)


@login_required
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

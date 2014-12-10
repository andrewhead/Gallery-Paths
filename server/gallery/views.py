# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count
from django.http import HttpResponseRedirect

import json
import jsonpickle
import datetime
from collections import defaultdict

from forms import ExhibitionForm, ExhibitForm
from models import Sighting, Exhibition, Exhibit


def index(request):
    context = {}
    return render(request, 'gallery/index.html')


def serialize(data):
    return jsonpickle.encode(data, unpicklable=False)


@login_required
def exhibits(request):

    def _getExhibitForms(exhibition, post=False, withFiles=False):
        forms = []
        ids = [e.id for e in Exhibit.objects.filter(user=request.user, exhibition=exhibition)]
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
        exhibition = Exhibition.objects.get(user=request.user, pk=request.POST.get('e', -1))
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
                f.instance.user = request.user
                f.save()
            return HttpResponseRedirect('exhibits?e=' + str(exhibition.pk))
        else:
            return render_to_response("gallery/exhibits.html", {
                "newForm": newForm,
                "forms": updateForms,
                "exhibition": exhibition,
            }, context_instance=RequestContext(request))

    if request.method == "GET":
        exhibition = Exhibition.objects.get(user=request.user, pk=request.GET.get('e', -1))
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

    exhibitions = Exhibition.objects.filter(user=request.user)

    if request.method == 'POST':
        if request.POST.get('action') == 'open':
            form = ExhibitionForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
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
            'exhibitions': Exhibition.objects.filter(user=request.user),
        }
        return render(request, 'gallery/exhibitions.html', context)


@login_required
def analytics(request):

    ''' Fetch exhibition and date bounds. '''
    exhibition = Exhibition.objects.get(
        user=request.user,
        id=request.GET.get('exhibition', -1)
    )
    start = exhibition.start
    end = exhibition.end or datetime.datetime.utcnow().date()
    exhibitIds = [e.location_id for e in Exhibit.objects.filter(exhibition=exhibition)]

    ''' Get base sightings with blacklisted values omitted. '''
    baseSightings = Sighting.objects.filter(
            client_id=request.user.id,
            location_id__in=exhibitIds
        ).exclude(location_id__in=[1111])

    ''' Get total event counts grouped by date. '''
    exhibitionSightings = baseSightings.filter(
        time__gte=start,
        time__lte=end + datetime.timedelta(days=1),  # add 1 day so we can get last day of exhibit
        )
    timesPerDate = list(exhibitionSightings
        .extra({'date': 'date(time)'})
        .values('date')
        .annotate(sighting_count=Count('id')))

    ''' Get events per exhibit at day, week, and month level. '''
    clientSightings = baseSightings.filter(
        time__lte=end + datetime.timedelta(days=1)
    )
    exhibitTimes = {}
    locationIds = set()
    timeGroups = {
        'day': max(exhibition.start, end),
        'week': max(exhibition.start, end - datetime.timedelta(days=7)),
        'all_time': exhibition.start,
    }
    for tg in timeGroups.keys():
        times = list(clientSightings
            .filter(time__gte=timeGroups[tg])
            .values('location_id')
            .annotate(totalTime=Count('location_id'))
            .order_by('-totalTime'))
        locationIds = locationIds.union([t['location_id'] for t in times])
        exhibitTimes[tg] = times

    ''' Compute bins of face widths for each location. '''
    locationDetectionWidths = Sighting.objects.raw('''
        SELECT id, location_id, wb, c FROM (
            SELECT id, ROUND((x3 - x1) / 10) AS wb, time, location_id, client_id, COUNT(*) AS c
            FROM gallery_sighting
            GROUP BY location_id, wb
            ORDER BY wb ASC
        ) AS temp 
        WHERE wb >= 0 AND 
            time >= '{start}' AND 
            time <= '{end}' AND 
            client_id = {clientId} AND 
            location_id IN ({locationList});
    '''.format(
        start=start.strftime("%Y%m%d"),
        end=end.strftime("%Y%m%d"),
        clientId=request.user.id,
        locationList=','.join([str(id_) for id_ in exhibitIds])
    ))
    widthBins = list(set(map(lambda ldw: ldw.wb, locationDetectionWidths)))
    widthBins = range(0, max(widthBins) + 1)
    detectionWidths = defaultdict(lambda: [0] * len(widthBins))
    for ldw in locationDetectionWidths:
        detectionWidths[ldw.location_id][int(ldw.wb)] = ldw.c
    detectionWidths = dict(detectionWidths)

    ''' Get thumbnails of all of the images to show. '''
    exhibitImages = {}
    exhibitNames = {}
    for l in locationIds:
        try:
            exhibit = Exhibit.objects.get(location_id=l, exhibition=exhibition)
        except Exhibit.DoesNotExist:
            continue
        exhibitImages[l] = '/media/' + exhibit.image.name
        exhibitNames[l] = exhibit.name

    context = {
        'timeByDay': serialize(timesPerDate),
        'trendTimes': serialize(exhibitTimes),
        'exhibitImages': serialize(exhibitImages),
        'exhibitNames': serialize(exhibitNames),
        'detectionWidths': serialize(detectionWidths),
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

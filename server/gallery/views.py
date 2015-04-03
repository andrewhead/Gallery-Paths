# encoding: utf-8

from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse

import json
import jsonpickle
import datetime
from collections import defaultdict

from forms import ExhibitionForm, ExhibitForm
from models import Sighting, Exhibition, Exhibit
from lookup import getExhibitionTimeBounds, getTimesPerDate, getExhibitImages, getDetectionWidths


def index(request):
    context = {}
    return render(request, 'gallery/index.html')


def serialize(data):
    return jsonpickle.encode(data, unpicklable=False)


@login_required
def exhibits(request, xid):

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
        exhibition = Exhibition.objects.get(user=request.user, pk=xid)
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
        exhibition = Exhibition.objects.get(user=request.user, pk=xid)
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
def analytics(request, xid):

    ''' Fetch exhibition and date bounds. '''
    exhibition = Exhibition.objects.get(user=request.user, id=xid)
    start, end = getExhibitionTimeBounds(exhibition)
    exhibits = Exhibit.objects.filter(exhibition=exhibition)
    locationIds = [e.location_id for e in Exhibit.objects.filter(exhibition=exhibition)]

    ''' Get base sightings with blacklisted values omitted. '''
    baseSightings = Sighting.objects.filter(
            client_id=request.user.id,
            location_id__in=locationIds
        ).exclude(location_id__in=[1111])

    ''' Get total event counts grouped by date. '''
    timesPerDate = getTimesPerDate(request.user.id, exhibition, locationIds, start, end)

    ''' Get events per exhibit at day, week, and month level. '''
    clientSightings = baseSightings.filter(
        upload_time__lte=end + datetime.timedelta(days=1)
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
            .filter(upload_time__gte=timeGroups[tg])
            .values('location_id')
            .annotate(totalTime=Count('location_id'))
            .order_by('-totalTime'))
        locationIds = locationIds.union([t['location_id'] for t in times])
        exhibitTimes[tg] = times
        for t in times:
            t['exhibit_id'] = Exhibit.objects.get(
                exhibition=exhibition,
                location_id=t['location_id']
            ).id

    ''' Compute bins of face widths for each location. '''
    detectionWidths = getDetectionWidths(request.user.id, exhibits, start, end)
    
    ''' Get thumbnails of all of the images to show. '''
    exhibitImages = getExhibitImages(exhibits)

    context = {
        'timeByDay': serialize(timesPerDate),
        'trendTimes': serialize(exhibitTimes),
        'exhibitImages': serialize(exhibitImages),
        'detectionWidths': serialize(detectionWidths),
        'exhibition': exhibition,
    }
    return render(request, 'gallery/analytics.html', context)


@login_required
def exhibit(request, eid):

    exhibit = Exhibit.objects.get(id=eid)
    locationId = exhibit.location_id
    exhibition = exhibit.exhibition
    if exhibition.user != request.user:
        return HttpResponse("Unauthorized", status=401)

    otherExhibits = [_ for _ in exhibition.exhibit_set.all()]
    exhibitIndex = otherExhibits.index(exhibit)
    nextIndex = (exhibitIndex + 1) % len(otherExhibits)
    prevIndex = (exhibitIndex - 1) % len(otherExhibits)

    ''' Fetch analytics. '''
    start, end = getExhibitionTimeBounds(exhibit.exhibition)
    timesPerDate = getTimesPerDate(request.user.id, exhibition, [locationId], start, end)
    detectionWidths = getDetectionWidths(request.user.id, [exhibit], start, end)

    exhibitLink = lambda index: '/exhibit/' + str(otherExhibits[index].id)
    context = {
        'name': exhibit.name,
        'thumbnail_url': exhibit.image.url,
        'next': exhibitLink(nextIndex),
        'prev': exhibitLink(prevIndex),
        'timesPerDate': serialize(timesPerDate),
        'exhibitImages': serialize(getExhibitImages([exhibit])),
        'detectionWidths': serialize(detectionWidths),
        'exhibition': exhibition,
    }
    return render(request, 'gallery/exhibit.html', context)


@login_required
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

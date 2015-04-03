#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.db.models import Count
import datetime
from collections import defaultdict

from gallery.models import Sighting, Exhibit


def getDetectionWidths(clientId, exhibits, start, end):
    ''' Assumes all exhibits belong to the same exhibition. '''
    exhibition = exhibits[0].exhibition
    locationIds = [e.location_id for e in exhibits]
    # Note: in the future, this should consider the upload time.  We don't know
    # how to handle it right now because of the time zone so we're skipping it currently.
    locationDetectionWidths = Sighting.objects.raw('''
        SELECT id, wb, upload_time, location_id, client_id, c FROM (
            SELECT id, ROUND((x3 - x1) / 10) AS wb, upload_time, location_id, client_id, COUNT(*) AS c
            FROM gallery_sighting
            GROUP BY client_id, location_id, wb
            ORDER BY wb ASC
        ) AS temp 
        WHERE wb >= 0 AND 
            client_id = {clientId} AND 
            location_id IN ({locationList});
    '''.format(
        clientId=clientId,
        locationList=','.join([str(l) for l in locationIds])
    ))
    widthBins = list(set(map(lambda ldw: ldw.wb, locationDetectionWidths)))
    if not widthBins:
        return {}
    widthBins = range(0, max(widthBins) + 1)
    detectionWidths = defaultdict(lambda: [0] * len(widthBins))
    for ldw in locationDetectionWidths:
        exhibit = Exhibit.objects.get(exhibition=exhibition, location_id=ldw.location_id)
        detectionWidths[int(exhibit.id)][int(ldw.wb)] = ldw.c
    detectionWidths = dict(detectionWidths)
    return detectionWidths


def getExhibitImages(exhibits):
    ''' Get lookup from location ID to exhibit image '''
    return {int(e.id): '/media/' + e.image.name for e in exhibits}


def getTimesPerDate(clientId, exhibition, locationIds, start, end):
    baseSightings = Sighting.objects.filter(
            client_id=clientId,
            location_id__in=locationIds
        ).exclude(location_id__in=[1111])
    exhibitionSightings = baseSightings.filter(
        upload_time__gte=start,
        upload_time__lte=end + datetime.timedelta(days=1),  # add 1 day so we can get last day of exhibit
        )
    timesPerDate = list(exhibitionSightings
        .extra({'date': 'date(upload_time)'})
        .values('date')
        .annotate(sighting_count=Count('id')))
    return timesPerDate


def getExhibitionTimeBounds(exhibition):
    start = exhibition.start
    end = exhibition.end or datetime.datetime.utcnow().date()
    return start, end

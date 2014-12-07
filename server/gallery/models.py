#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.db import models
from time import strftime


def upload_image_to(inst, fn):
    base = '.'.join(fn.split('.')[:-1])
    ext = fn.split('.')[-1]
    return base + '-' + strftime("%Y%m%d%H%M%S") + '.' + ext


class Sighting(models.Model):
    ''' Event where a museum visitor is detected. '''
    time = models.DateTimeField()
    client_id = models.IntegerField()
    location_id = models.PositiveSmallIntegerField()
    visitor_id = models.IntegerField()
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    x3 = models.IntegerField()
    y3 = models.IntegerField()


class Exhibition(models.Model):
    ''' Collection of works displayed for a period of time. '''
    name = models.CharField(max_length=255)
    start = models.DateField(auto_now_add=True)
    end = models.DateField(default=None, blank=True, null=True)


class Exhibit(models.Model):
    ''' Work of art in a gallery. '''
    name = models.CharField(max_length=255)
    exhibition = models.ForeignKey(Exhibition)
    location_id = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to=upload_image_to)

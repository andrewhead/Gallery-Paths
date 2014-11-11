#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.db import models


class Sighting(models.Model):
    user_id = models.IntegerField()
    painting_id = models.IntegerField()
    time = models.DateTimeField()
    x1 = models.IntegerField()
    x2 = models.IntegerField()
    y1 = models.IntegerField()
    y2 = models.IntegerField()

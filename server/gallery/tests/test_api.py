#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from tastypie.test import ResourceTestCase
from gallery.models import Sighting


class PostSightingTest(ResourceTestCase):

    def testPostAddsOneSighting(self):
        self.assertEqual(Sighting.objects.count(), 0)
        self.assertHttpCreated(self.api_client.post(
            '/api/sighting/', format='json', data={
                'user_id': 1111,
                'painting_id': 2222,
                'time': '2014-10-31T12:34:56',
                'x1': 10,
                'x2': 20,
                'y1': 5,
                'y2': 15,
            }))
        self.assertEqual(Sighting.objects.count(), 1)

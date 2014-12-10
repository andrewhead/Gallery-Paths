# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0009_auto_20141207_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='sighting',
            name='upload_time',
            field=models.DateTimeField(default=None, auto_now_add=True),
            preserve_default=False,
        ),
    ]

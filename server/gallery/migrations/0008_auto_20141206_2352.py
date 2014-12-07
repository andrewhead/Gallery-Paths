# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_exhibit_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibit',
            name='location_id',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sighting',
            name='location_id',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
    ]

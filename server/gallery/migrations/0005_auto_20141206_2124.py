# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_exhibit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibit',
            name='image',
            field=models.ImageField(null=True, upload_to=gallery.models.upload_image_to, blank=True),
            preserve_default=True,
        ),
    ]

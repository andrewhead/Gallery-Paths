# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20141206_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibit',
            name='image',
            field=models.ImageField(upload_to=gallery.models.upload_image_to),
            preserve_default=True,
        ),
    ]

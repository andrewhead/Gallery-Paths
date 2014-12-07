# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_auto_20141206_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibit',
            name='name',
            field=models.CharField(default='Unnamed', max_length=255),
            preserve_default=False,
        ),
    ]

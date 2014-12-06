# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_exhibition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibition',
            name='end',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('client_id', models.IntegerField()),
                ('location_id', models.IntegerField()),
                ('visitor_id', models.IntegerField()),
                ('x1', models.IntegerField()),
                ('y1', models.IntegerField()),
                ('x2', models.IntegerField()),
                ('y2', models.IntegerField()),
                ('x3', models.IntegerField()),
                ('y3', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

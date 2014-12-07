# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20141206_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exhibit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_id', models.IntegerField()),
                ('image', models.ImageField(upload_to=gallery.models.upload_image_to)),
                ('exhibition', models.ForeignKey(to='gallery.Exhibition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

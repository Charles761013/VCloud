# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-14 15:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='length',
        ),
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-09 07:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('eforce_api', '0014_auto_20170909_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='crisis',
            name='cmo_crisis_id',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crisis',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 9, 9, 7, 34, 1, 775121, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

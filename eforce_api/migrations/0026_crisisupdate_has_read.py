# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-27 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eforce_api', '0025_remove_groupinstruction_resolve'),
    ]

    operations = [
        migrations.AddField(
            model_name='crisisupdate',
            name='has_read',
            field=models.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-23 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import eforce_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('eforce_api', '0021_auto_20170923_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='groupimage',
            field=models.ImageField(blank=True, null=True, upload_to=eforce_api.models.group_image_directory_path),
        ),
    ]
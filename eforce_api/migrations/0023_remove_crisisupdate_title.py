# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-23 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eforce_api', '0022_usergroup_groupimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crisisupdate',
            name='title',
        ),
    ]

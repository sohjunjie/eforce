# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-09 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eforce_api', '0006_auto_20170909_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemgroup',
            name='instruction',
            field=models.ManyToManyField(through='eforce_api.InstructionGroupAssoc', to='eforce_api.GroupInstruction'),
        ),
    ]

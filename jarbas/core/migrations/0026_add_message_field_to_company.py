# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_rename_json_activities_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='message',
            field=models.CharField(blank=True, max_length=140, null=True, verbose_name='Message'),
        ),
    ]

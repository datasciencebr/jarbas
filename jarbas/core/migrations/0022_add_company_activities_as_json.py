# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 14:46
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_make_reciept_fetched_a_db_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='json_main_activity',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='main_activity'),
        ),
        migrations.AddField(
            model_name='company',
            name='json_secondary_activity',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='secondary_activity'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 07:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0021_auto_20170329_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientgroup',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

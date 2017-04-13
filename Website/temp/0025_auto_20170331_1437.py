# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 06:37
from __future__ import unicode_literals

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0024_auto_20170331_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorinfo',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='doctorinfo',
            name='userName',
        ),
        migrations.AddField(
            model_name='doctorinfo',
            name='username',
            field=models.CharField(default='default', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doctorinfo',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]

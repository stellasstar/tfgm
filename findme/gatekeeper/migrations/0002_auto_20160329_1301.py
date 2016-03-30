# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gatekeeper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date_joined',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created'),
        ),
    ]
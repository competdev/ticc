# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-07 23:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_auto_20170206_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchscore',
            name='responsible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

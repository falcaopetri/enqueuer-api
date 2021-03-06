# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 20:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20161005_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='api.Queue'),
        ),
        migrations.AlterField(
            model_name='queue',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queues', to='api.User'),
        ),
    ]

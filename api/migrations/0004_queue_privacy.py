# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-15 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20161008_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='privacy',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], default='private', max_length=20),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 00:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_queue_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='name',
            field=models.CharField(default='name', max_length=30),
            preserve_default=False,
        ),
    ]

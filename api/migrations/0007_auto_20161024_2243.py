# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 00:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20161015_2113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='media',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.User'),
            preserve_default=False,
        ),
    ]

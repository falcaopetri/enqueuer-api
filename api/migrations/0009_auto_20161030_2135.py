# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 23:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_media_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserProfile',
        ),
    ]

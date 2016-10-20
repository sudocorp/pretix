# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 17:57
from __future__ import unicode_literals

import pytz
from django.db import migrations
from django.utils import timezone


def forwards(apps, schema_editor):
    Order = apps.get_model('pretixbase', 'Order')
    EventSetting = apps.get_model('pretixbase', 'EventSetting')
    etz = {
        s['object_id']: s['value']
        for s in EventSetting.objects.filter(key='timezone').values('object_id', 'value')
    }
    for order in Order.objects.all():
        tz = pytz.timezone(etz.get(order.event_id, 'UTC'))
        order.expires = order.expires.astimezone(tz).replace(hour=23, minute=59, second=59)
        order.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0041_auto_20161018_1654'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]

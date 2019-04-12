# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-10 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hgw_backend', '0002_add_oauth2_basic_auth'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailedConnector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1500)),
                ('reason', models.CharField(choices=[('JS', 'JSON_ENCODING'), ('SN', 'SOURCE_NOT_FOUND'), ('WS', 'WRONG_MESSAGE_STRUCTURE'), ('SE', 'SENDING_ERROR')], max_length=2)),
                ('retry', models.BooleanField()),
            ],
        ),
    ]

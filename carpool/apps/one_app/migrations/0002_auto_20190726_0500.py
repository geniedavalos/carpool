# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-26 05:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='from',
            name='rider',
            field=models.ManyToManyField(related_name='riders', to='one_app.User'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 14:00
from __future__ import unicode_literals

import cel.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cel', '0003_auto_20170302_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='modified',
            field=cel.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
    ]

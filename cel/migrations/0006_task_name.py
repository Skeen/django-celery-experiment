# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cel', '0005_task_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_fsm_log', '0002_auto_20151207_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statelog',
            name='object_id',
            field=models.CharField(max_length=32, db_index=True),
        ),
    ]

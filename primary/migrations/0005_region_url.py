# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0004_auto_20150428_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='url',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0006_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='motto',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='platform1',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='platform2',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]

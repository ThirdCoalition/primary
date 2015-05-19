# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0009_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='platform1',
        ),
        migrations.RemoveField(
            model_name='usersettings',
            name='platform2',
        ),
        migrations.AddField(
            model_name='usersettings',
            name='platform',
            field=models.CharField(default=b'', max_length=2000),
        ),
    ]

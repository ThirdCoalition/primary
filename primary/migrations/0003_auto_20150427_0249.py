# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0002_usersettings_handle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='handle',
            field=models.CharField(default=b'', unique=True, max_length=20),
        ),
    ]

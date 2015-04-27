# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='handle',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]

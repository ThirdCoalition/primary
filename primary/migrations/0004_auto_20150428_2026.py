# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0003_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='region',
            field=models.ForeignKey(default=1, to='primary.Region'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersettings',
            name='region',
            field=models.ForeignKey(default=1, to='primary.Region'),
            preserve_default=False,
        ),
    ]

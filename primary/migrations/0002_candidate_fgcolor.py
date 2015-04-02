# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='fgcolor',
            field=models.CharField(default='blah', max_length=30),
            preserve_default=False,
        ),
    ]

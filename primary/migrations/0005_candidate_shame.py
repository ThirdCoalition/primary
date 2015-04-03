# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0004_sums'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='shame',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

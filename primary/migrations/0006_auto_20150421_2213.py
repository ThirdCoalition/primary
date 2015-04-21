# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0005_candidate_shame'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='shame',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

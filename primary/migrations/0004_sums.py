# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0003_auto_20150402_0533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sums',
            fields=[
                ('candidate_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='primary.Candidate')),
                ('approval', models.IntegerField()),
            ],
            options={
                'ordering': ['-approval'],
                'managed': False,
            },
            bases=('primary.candidate',),
        ),
    ]

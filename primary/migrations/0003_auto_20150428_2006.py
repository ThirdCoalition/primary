# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primary', '0002_usersettings_handle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('synopsis', models.CharField(max_length=500)),
                ('logo', models.URLField()),
                ('link', models.URLField()),
                ('color', models.CharField(max_length=30)),
                ('fgcolor', models.CharField(max_length=30)),
                ('shame', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(default=b'', max_length=10)),
                ('delegate', models.ForeignKey(related_name='delegate', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
        migrations.AddField(
            model_name='approval',
            name='candidate',
            field=models.ForeignKey(to='primary.Candidate'),
        ),
        migrations.AddField(
            model_name='approval',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

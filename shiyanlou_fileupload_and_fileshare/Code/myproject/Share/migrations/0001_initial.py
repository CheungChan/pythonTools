# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DownloadDocument', models.IntegerField(default=0)),
                ('code', models.CharField(max_length=8)),
                ('Datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('path', models.CharField(max_length=32)),
                ('name', models.CharField(default=b'', max_length=32)),
                ('Filesize', models.CharField(max_length=10)),
                ('PCIP', models.CharField(default=b'', max_length=32)),
            ],
            options={
                'db_table': 'download',
                'verbose_name': 'download',
            },
        ),
    ]

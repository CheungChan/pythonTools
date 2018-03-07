# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Share', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upload',
            old_name='DownloadDocument',
            new_name='DownloadDoccount',
        ),
        migrations.AlterField(
            model_name='upload',
            name='PCIP',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='upload',
            name='name',
            field=models.CharField(default='', max_length=32),
        ),
    ]

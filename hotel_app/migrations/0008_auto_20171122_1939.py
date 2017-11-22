# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_app', '0007_auto_20171108_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estate',
            name='image',
            field=models.ImageField(max_length=200, blank=True, null=True, upload_to='image'),
        ),
    ]

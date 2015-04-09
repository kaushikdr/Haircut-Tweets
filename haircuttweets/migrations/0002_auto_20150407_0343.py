# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haircuttweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetssearched',
            name='tweets_result',
            field=models.CharField(max_length=10485760, blank=True),
        ),
    ]

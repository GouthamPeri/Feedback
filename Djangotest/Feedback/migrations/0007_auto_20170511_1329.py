# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-11 07:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Feedback', '0006_auto_20170511_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseregistration',
            name='student_reg_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='Feedback.Student'),
        ),
    ]

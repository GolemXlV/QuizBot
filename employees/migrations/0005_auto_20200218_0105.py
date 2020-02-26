# Generated by Django 2.2 on 2020-02-18 01:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_employee_days_for_poll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='days_for_poll',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], default=['1', '2', '3', '4', '5', '6', '7'], max_length=1, verbose_name='Days for poll'), size=None, verbose_name='Days for poll'),
        ),
    ]
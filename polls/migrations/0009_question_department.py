# Generated by Django 2.2 on 2020-02-25 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_auto_20200225_1117'),
        ('polls', '0008_auto_20200225_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.Department', verbose_name='Department'),
        ),
    ]

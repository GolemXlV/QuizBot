# Generated by Django 2.2 on 2020-02-11 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200211_1103'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='poll',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='question',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='poll',
            name='date_closed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date closed'),
        ),
    ]

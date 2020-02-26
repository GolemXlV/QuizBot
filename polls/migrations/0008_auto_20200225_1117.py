# Generated by Django 2.2 on 2020-02-25 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20200218_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.TextField(max_length=500, verbose_name='Answer text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(max_length=500, verbose_name='Question text'),
        ),
    ]
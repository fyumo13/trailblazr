# Generated by Django 3.0.6 on 2020-05-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trailblazr', '0004_auto_20200508_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trail',
            name='ascent',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trail',
            name='descent',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trail',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trail',
            name='length',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trail',
            name='lon',
            field=models.FloatField(default=0),
        ),
    ]
# Generated by Django 5.0.7 on 2024-08-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subathonTimer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='bonus_time',
            field=models.ManyToManyField(to='subathonTimer.bonustime'),
        ),
    ]

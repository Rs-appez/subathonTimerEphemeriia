# Generated by Django 5.0.8 on 2024-09-16 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subathonTimer', '0005_subgoal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='timer_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timer',
            name='timer_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
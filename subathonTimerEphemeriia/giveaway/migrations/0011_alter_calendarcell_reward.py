# Generated by Django 5.1.9 on 2025-05-22 21:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giveaway', '0010_remove_reward_image_url_alter_reward_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarcell',
            name='reward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='giveaway.reward'),
        ),
    ]

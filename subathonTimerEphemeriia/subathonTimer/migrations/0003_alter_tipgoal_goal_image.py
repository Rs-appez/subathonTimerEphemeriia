# Generated by Django 5.0.8 on 2024-09-12 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subathonTimer', '0002_tipgoal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipgoal',
            name='goal_image',
            field=models.ImageField(upload_to='subathonTimerEphemeriia/static/subathonTimer/images/'),
        ),
    ]

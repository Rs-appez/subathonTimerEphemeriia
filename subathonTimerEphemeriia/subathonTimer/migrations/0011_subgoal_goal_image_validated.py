# Generated by Django 5.1.6 on 2025-03-02 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subathonTimer', '0010_alter_tipgoal_goal_image_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='subgoal',
            name='goal_image_validated',
            field=models.ImageField(blank=True, null=True, upload_to='subathonTimerEphemeriia/static/subathonTimer/images/subs/validated/'),
        ),
    ]

# Generated by Django 5.0.8 on 2024-08-10 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_alter_streamlabsauth_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamlabsauth',
            name='refresh_token',
            field=models.CharField(max_length=2083),
        ),
        migrations.AlterField(
            model_name='streamlabsauth',
            name='socket_token',
            field=models.CharField(max_length=2083),
        ),
    ]

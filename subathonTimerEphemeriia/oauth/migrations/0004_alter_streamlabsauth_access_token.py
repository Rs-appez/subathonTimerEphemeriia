# Generated by Django 5.0.8 on 2024-08-10 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0003_alter_streamlabsauth_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamlabsauth',
            name='access_token',
            field=models.CharField(max_length=2083),
        ),
    ]
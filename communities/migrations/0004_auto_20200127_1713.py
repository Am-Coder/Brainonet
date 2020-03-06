# Generated by Django 2.2.5 on 2020-01-27 17:13

import communities.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_auto_20191228_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communities',
            name='avatarimage',
            field=models.ImageField(upload_to=communities.models.upload_location_avatarimage),
        ),
        migrations.AlterField(
            model_name='communities',
            name='backgroundimage',
            field=models.ImageField(upload_to=communities.models.upload_location_backgroundimage),
        ),
        migrations.AlterField(
            model_name='communities',
            name='description',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='communities',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
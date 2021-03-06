# Generated by Django 2.2.2 on 2019-12-25 18:42

import communities.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Communties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True, max_length=5000)),
                ('backgroundimage', models.ImageField(blank=True, upload_to=communities.models.upload_location_backgroundimage)),
                ('avatarimage', models.ImageField(upload_to=communities.models.upload_location_avatarimage)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
    ]

# Generated by Django 2.2.2 on 2019-12-28 15:47

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0003_auto_20191228_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('body', models.TextField(blank=True, max_length=5000)),
                ('image', models.ImageField(blank=True, upload_to=blog.models.upload_location)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communities.Communities')),
            ],
        ),
    ]
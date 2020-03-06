# Generated by Django 2.2.5 on 2020-01-27 17:13

from django.db import migrations, models
import exposeunits.models


class Migration(migrations.Migration):

    dependencies = [
        ('exposeunits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposeunits',
            name='avatarimage',
            field=models.ImageField(upload_to=exposeunits.models.upload_location_avatarimage),
        ),
        migrations.AlterField(
            model_name='exposeunits',
            name='backgroundimage',
            field=models.ImageField(upload_to=exposeunits.models.upload_location_backgroundimage),
        ),
        migrations.AlterField(
            model_name='exposeunits',
            name='description',
            field=models.TextField(max_length=5000),
        ),
    ]
# Generated by Django 2.2.5 on 2020-03-27 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20200327_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='references',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

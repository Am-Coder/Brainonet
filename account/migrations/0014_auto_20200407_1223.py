# Generated by Django 2.2.5 on 2020-04-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20200207_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(default='', max_length=30, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(default='', max_length=30, null=True, verbose_name='last name'),
        ),
    ]

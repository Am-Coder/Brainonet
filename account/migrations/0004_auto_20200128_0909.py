# Generated by Django 2.2.5 on 2020-01-28 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_account_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='token',
        ),
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=30, null=True, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='account',
            name='mobile_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

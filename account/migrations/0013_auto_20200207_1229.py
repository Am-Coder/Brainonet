# Generated by Django 2.2.5 on 2020-02-07 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20200131_1911'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['date_joined']},
        ),
    ]

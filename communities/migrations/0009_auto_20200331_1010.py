# Generated by Django 2.2.5 on 2020-03-31 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0008_auto_20200331_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityhistory',
            name='communityid',
            field=models.CharField(max_length=10),
        ),
    ]

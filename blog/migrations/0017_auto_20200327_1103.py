# Generated by Django 2.2.5 on 2020-03-27 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20200327_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='references',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
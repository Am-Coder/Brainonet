# Generated by Django 2.2.5 on 2020-03-27 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_blog_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='references',
            name='description',
            field=models.CharField(default=None, max_length=100),
        ),
    ]

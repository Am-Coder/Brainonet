# Generated by Django 2.2.5 on 2020-03-31 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0022_auto_20200328_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('job', models.CharField(choices=[('C', 'Create'), ('U', 'Update'), ('D', 'Delete')], max_length=15)),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.References')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('job', models.CharField(choices=[('C', 'Create'), ('U', 'Update'), ('D', 'Delete')], max_length=15)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
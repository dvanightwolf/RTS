# Generated by Django 4.0.5 on 2022-06-03 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='city',
        ),
    ]
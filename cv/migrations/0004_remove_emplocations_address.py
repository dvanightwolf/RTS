# Generated by Django 3.2.9 on 2022-05-15 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0003_auto_20220512_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emplocations',
            name='address',
        ),
    ]

# Generated by Django 3.2.9 on 2022-05-15 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20220512_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locations',
            name='address',
        ),
    ]

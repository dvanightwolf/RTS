# Generated by Django 4.0.5 on 2022-06-03 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0005_cv_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emplocations',
            name='city',
        ),
    ]

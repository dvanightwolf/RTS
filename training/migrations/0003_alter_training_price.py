# Generated by Django 3.2.9 on 2022-06-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_remove_training_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

# Generated by Django 3.2.9 on 2022-05-15 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0004_remove_emplocations_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='cv',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=15),
        ),
    ]
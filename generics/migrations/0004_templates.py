# Generated by Django 3.2.9 on 2022-06-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generics', '0003_delete_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=30)),
            ],
        ),
    ]

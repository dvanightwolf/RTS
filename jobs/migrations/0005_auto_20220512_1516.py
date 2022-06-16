# Generated by Django 3.2.9 on 2022-05-12 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generics', '0001_initial'),
        ('jobs', '0004_alter_requiredskills_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirededucation',
            name='education',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generics.educations'),
        ),
        migrations.AlterField(
            model_name='requiredexperience',
            name='experience',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generics.experiences'),
        ),
    ]
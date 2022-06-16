# Generated by Django 3.2.9 on 2022-05-12 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generics', '0001_initial'),
        ('cv', '0002_auto_20220512_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empeducations',
            name='education',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generics.educations'),
        ),
        migrations.AlterField(
            model_name='empexperience',
            name='experience',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generics.experiences'),
        ),
        migrations.AlterField(
            model_name='empskills',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generics.skills'),
        ),
    ]
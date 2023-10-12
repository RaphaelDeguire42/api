# Generated by Django 4.2.3 on 2023-08-04 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customModels', '0009_project_foldername'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='forfait',
        ),
        migrations.AddField(
            model_name='customuser',
            name='jetons',
            field=models.BigIntegerField(default=0, verbose_name='jetons'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='jetons_or',
            field=models.BigIntegerField(default=0, verbose_name='jetons_or'),
        ),
        migrations.DeleteModel(
            name='Forfait',
        ),
    ]

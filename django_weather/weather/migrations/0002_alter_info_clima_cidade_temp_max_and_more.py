# Generated by Django 5.1 on 2024-10-22 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info_clima_cidade',
            name='temp_max',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='info_clima_cidade',
            name='temp_min',
            field=models.IntegerField(default=0),
        ),
    ]

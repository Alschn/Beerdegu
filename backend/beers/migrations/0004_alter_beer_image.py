# Generated by Django 4.2.4 on 2023-08-03 11:58

import beers.models.beer
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0003_alter_beer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=beers.models.beer.get_file_path),
        ),
    ]

# Generated by Django 3.2.5 on 2021-07-13 12:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0003_auto_20210713_1250'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='beers',
            field=models.ManyToManyField(blank=True, through='rooms.BeerInRoom', to='beers.Beer'),
        ),
        migrations.AlterField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(blank=True, through='rooms.UserInRoom', to=settings.AUTH_USER_MODEL),
        ),
    ]

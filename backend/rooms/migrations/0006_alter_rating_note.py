# Generated by Django 3.2.5 on 2021-07-17 17:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_userinroom_last_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='note',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]

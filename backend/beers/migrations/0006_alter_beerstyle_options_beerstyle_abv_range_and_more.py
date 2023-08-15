# Generated by Django 4.2.4 on 2023-08-15 10:14

import django.contrib.postgres.fields.ranges
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('beers', '0005_alter_brewery_options_remove_brewery_established_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beerstyle',
            options={'verbose_name': 'Beer Style', 'verbose_name_plural': 'Beer Styles'},
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='known_as',
            field=models.CharField(
                blank=True, help_text='Other names for this beer style (comma separated)',
                max_length=255, null=True
            ),
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='abv_range',
            field=django.contrib.postgres.fields.ranges.DecimalRangeField(
                blank=True,
                help_text='Alcohol by volume measured in percentages',
                null=True)
            ,
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='bitterness_range',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(
                blank=True,
                help_text='Bitterness described in IBU (International Bitterness Units)',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='color_range',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(
                blank=True,
                help_text='Color described in EBC (European Brewery Convention) units',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='final_gravity_range',
            field=django.contrib.postgres.fields.ranges.DecimalRangeField(
                blank=True,
                help_text='Final gravity measured in degrees Plato',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='original_gravity_range',
            field=django.contrib.postgres.fields.ranges.DecimalRangeField(
                blank=True,
                help_text='Original gravity measured in degrees Plato',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='beerstyle',
            name='serving_temperature_range',
            field=django.contrib.postgres.fields.ranges.DecimalRangeField(
                blank=True,
                help_text='Temperature measured in Celsius',
                null=True
            ),
        ),
    ]
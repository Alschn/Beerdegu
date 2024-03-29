# Generated by Django 4.2.4 on 2023-08-15 10:53

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('beers', '0006_alter_beerstyle_options_beerstyle_abv_range_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hop',
            options={'verbose_name': 'Hop', 'verbose_name_plural': 'Hops'},
        ),
        migrations.AlterField(
            model_name='hop',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]

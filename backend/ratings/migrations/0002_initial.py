# Generated by Django 4.2.4 on 2023-08-12 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ratings', '0001_initial'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ratings', to='rooms.room'),
        ),
    ]
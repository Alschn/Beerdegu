# Generated by Django 3.2.5 on 2021-07-16 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_alter_beerinroom_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinroom',
            name='last_active',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

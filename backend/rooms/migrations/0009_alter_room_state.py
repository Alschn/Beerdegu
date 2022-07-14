# Generated by Django 4.0.5 on 2022-07-14 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0008_alter_room_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='state',
            field=models.CharField(choices=[('WAITING', 'Waiting'), ('STARTING', 'Starting'), ('IN_PROGRESS', 'In progress'), ('FINISHED', 'Finished')], default='WAITING', max_length=11),
        ),
    ]
# Generated by Django 5.0 on 2024-04-22 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_event_organizer_event_organizer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='organizer',
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
        ),
    ]

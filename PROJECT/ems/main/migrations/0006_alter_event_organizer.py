# Generated by Django 5.0 on 2024-04-22 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_event_organizer_event_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
        ),
    ]
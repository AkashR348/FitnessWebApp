# Generated by Django 5.1.3 on 2024-11-21 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='total_time',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

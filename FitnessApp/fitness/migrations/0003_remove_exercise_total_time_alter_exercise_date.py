# Generated by Django 5.1.2 on 2024-11-26 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_exercise_total_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='total_time',
        ),
        migrations.AlterField(
            model_name='exercise',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
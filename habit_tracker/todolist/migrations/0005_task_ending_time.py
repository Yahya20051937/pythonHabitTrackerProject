# Generated by Django 4.2.2 on 2023-06-14 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_remove_task_ending_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='ending_time',
            field=models.TimeField(default='00:00:00', max_length=10),
        ),
    ]

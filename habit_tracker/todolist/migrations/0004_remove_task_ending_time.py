# Generated by Django 4.2.2 on 2023-06-14 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_rename_time_task_starting_time_task_ending_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='ending_time',
        ),
    ]

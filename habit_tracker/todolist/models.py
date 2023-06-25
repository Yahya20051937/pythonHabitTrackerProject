from django.db import models
import time
from django.contrib.auth.models import User


# Create your models here.
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    day = models.CharField(max_length=20)


class Task(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    # starting_time = models.TimeField(max_length=10, default="00:00:00")
    # ending_time = models.TimeField(max_length=10, default="00:00:00")
    time = models.CharField(max_length=200, default='skip-skip')
    rate = models.IntegerField(default=1)
    performance = models.CharField(default='good', max_length=15)

    bool_check = models.BooleanField(default=False)

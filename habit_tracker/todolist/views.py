import django.db.utils
from django.shortcuts import render
import logging, os
from pathlib import Path
from functions import decode, get_time

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect
from .models import ToDoList, Task

logging.basicConfig(format='%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d] %(message)s', datefmt='%d-%m-%Y '
                                                                                                       '%H:%M:%S ',
                    level=logging.CRITICAL,
                    filename='logs.txt')
logger = logging.getLogger('userathlogs')

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.

def home_page(request, encoded_id, day):
    from .helping_functions import modify_performance, get_style_tag, transform_underscore_to_slash, \
        transform_slash_to_underscore, get_image_base64
    from habit_tracking.helping_function import get_day_performance
    from database import DataBaseManagement, edit_info
    decoded_id = decode(encoded_id)
    day = transform_underscore_to_slash(day)
    logger.critical(day)
    logger.critical(f'id : {decoded_id}')
    user = User.objects.get(id=decoded_id)

    # render a table that has the task of the user for this day
    try:

        all_todo_lists = list(user.todolist_set.all())
        today_todolist = list(filter(lambda x: x.day == day, all_todo_lists))[0]
    except IndexError:

        today_todolist = ToDoList.objects.create(user=user, day=day)
        today_todolist.save()

    tasks = list(today_todolist.task_set.all())

    modify_performance(decoded_id, tasks)
    style_tag = get_style_tag()  # function provided by CHAT-GPT to style the th tags

    if request.method == 'POST':

        checked_tasks = request.POST.getlist('bool_check')

        # this code is for checking tasks
        for task_id in checked_tasks:
            task = list(filter(lambda x: x.id == int(task_id), tasks))[0]
            task.bool_check = True
            with DataBaseManagement(decoded_id) as connection:
                edit_info(connection, task.name, day)
            task.save()
        # this code is for unchecking tasks
        for task in tasks:
            if task.id not in [int(my_id) for my_id in checked_tasks]:
                task.bool_check = False
                task.save()

    day = transform_slash_to_underscore(day)
    day_performance = get_day_performance(
        tasks)  # this variable will hold the performance until this moment, and will be used in the bar graph
    image_base64 = get_image_base64(day_performance)
    logger.critical(day)
    return render(request, 'todolist/home_page.html',
                  {"day": day, "tasks": tasks, "encoded_id": encoded_id,
                   'style_tag': style_tag,
                   'days_range': range(1, 32), 'month_range': range(1, 13), 'year_range': range(1, 30), 'image_base64':image_base64})


def delete_page(request, encoded_id, day):
    from .helping_functions import transform_underscore_to_slash, transform_slash_to_underscore

    decoded_id = decode(encoded_id)
    user = User.objects.get(id=decoded_id)
    day = transform_underscore_to_slash(day)
    all_todo_lists = list(user.todolist_set.all())
    today_todolist = list(filter(lambda x: x.day == day, all_todo_lists))[0]
    tasks = list(today_todolist.task_set.all())
    day = transform_slash_to_underscore(day)
    if request.method == 'POST':
        tasks_to_delete_ids = request.POST.getlist('to_delete')
        for task_id in tasks_to_delete_ids:
            task = list(filter(lambda x: x.id == int(task_id), tasks))[0]
            task.delete()
        return redirect(f'/user_home_page/{encoded_id}/{day}')
    return render(request, 'todolist/delete_page.html',

                  {"day": day, "tasks": tasks, "encoded_id": encoded_id})


def edit_page(request, encoded_id, day):
    from .helping_functions import transform_underscore_to_slash, transform_slash_to_underscore
    from database import DataBaseManagement, edit_info, get_info

    decoded_id = decode(encoded_id)
    day = transform_underscore_to_slash(day)
    user = User.objects.get(id=decoded_id)
    all_todo_lists = list(user.todolist_set.all())
    today_todolist = list(filter(lambda x: x.day == day, all_todo_lists))[0]
    tasks = list(today_todolist.task_set.all())

    with DataBaseManagement(decoded_id) as conn:   # code to show the rate in the template
        for task in tasks:
            task.rate = get_info(conn, task.name, 'rate')

    day = transform_slash_to_underscore(day)
    if request.method == 'POST':
        for task_id in [t.id for t in tasks]:
            task = Task.objects.get(id=task_id)

            new_name = request.POST.get(f'{task_id}/name')
            task.name = new_name

            new_starting_time = request.POST.get(f'{task_id}/starting_time')
            if request.POST.get('skipping_check') != 'skip':
                new_ending_time = request.POST.get(f'{task_id}/ending_time')

                task.time = f'{new_starting_time}-{new_ending_time}'
            else:
                task.time = f'{new_starting_time}-'

            new_task_rate = request.POST.get(f'{task_id}/rate') or 1
            with DataBaseManagement(decoded_id) as connection:
                edit_info(connection, task.name, day, int(new_task_rate), False)

            task.save()
        return redirect(f'/user_home_page/{encoded_id}/{day}')

    return render(request, 'todolist/edit_page.html',
                  {"day": day, "tasks": tasks, "encoded_id": encoded_id})


def add_page(request, encoded_id, day):
    from .helping_functions import transform_underscore_to_slash, transform_slash_to_underscore
    from database import DataBaseManagement, get_all_tasks

    decoded_id = decode(encoded_id)
    user = User.objects.get(id=decoded_id)
    day = transform_underscore_to_slash(day)
    today_todolist = ToDoList.objects.get(user=user, day=day)
    tasks = list(today_todolist.task_set.all())
    with DataBaseManagement(decoded_id) as conn:
        user_habits = get_all_tasks(conn)      # this list hold the options that the user can choose as the name of its task
    day = transform_slash_to_underscore(day)

    if request.method == "POST":
        task_name = request.POST.get('name')
        starting_time = request.POST.get('starting_time')
        if request.POST.get('skipping_box') != 'skip':
            ending_time = request.POST.get("ending_time")
            time = f'{starting_time}-{ending_time}'
        else:
            time = f'{starting_time}-'
        task = Task.objects.create(todolist=today_todolist, name=task_name, time=time,
                                   bool_check=False)
        task.save()
        return redirect(f'/user_home_page/{encoded_id}/{day}')

    return render(request, 'todolist/add_page.html',
                  {"day": day, "tasks": tasks, "encoded_id": encoded_id, 'habits':user_habits})


def change_day(request, encoded_id):
    from .helping_functions import get_day_from_request

    new_day = get_day_from_request(request)
    return redirect(f'/user_home_page/{encoded_id}/{new_day}')


def add_new_habit(request, encoded_id, day):  # this function will be used to let the user add a new habit
    from database import DataBaseManagement, edit_info
    from functions import decode

    decoded_id = decode(encoded_id)

    if request.method == 'POST':
        with DataBaseManagement(decoded_id) as conn:
            habit_name = request.POST.get('name')
            habit_rate = int(request.POST.get('rate'))
            edit_info(conn, day, habit_name, habit_rate)
        return redirect(f'/user_home_page/{encoded_id}/{day}')
    return render(request, 'todolist/add_habit.html')


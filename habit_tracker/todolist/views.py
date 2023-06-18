import django.db.utils
from django.shortcuts import render
import logging, os
from pathlib import Path
from .helping_functions import get_time

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

def home_page(request, encoded_id):
    from functions import decode
    decoded_id = decode(encoded_id)
    day = get_time()
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

    if request.method == 'POST':
        checked_tasks = request.POST.getlist('bool_check')
        logger.critical(checked_tasks)
        # this code is for checking tasks
        for task_id in checked_tasks:
            task = list(filter(lambda x: x.id == int(task_id), tasks))[0]
            task.bool_check = True
            task.save()
        # this code is for unchecking tasks
        for task in tasks:
            if task.id not in [int(my_id) for my_id in checked_tasks]:
                task.bool_check = False
                task.save()

    return render(request, 'todolist/home_page.html',
                  {"day": today_todolist.day, "tasks": tasks, "encoded_id": encoded_id})


def delete_page(request, encoded_id):
    from functions import decode
    decoded_id = decode(encoded_id)
    user = User.objects.get(id=decoded_id)
    day = get_time()
    all_todo_lists = list(user.todolist_set.all())
    today_todolist = list(filter(lambda x: x.day == day, all_todo_lists))[0]
    tasks = list(today_todolist.task_set.all())

    if request.method == 'POST':
        tasks_to_delete_ids = request.POST.getlist('to_delete')
        for task_id in tasks_to_delete_ids:
            task = list(filter(lambda x: x.id == int(task_id), tasks))[0]
            task.delete()
        return redirect(f'/user_home_page/{encoded_id}')
    return render(request, 'todolist/delete_page.html',
                  {"day": today_todolist.day, "tasks": tasks, "encoded_id": encoded_id})


def edit_page(request, encoded_id):
    from functions import decode
    decoded_id = decode(encoded_id)
    day = get_time()
    user = User.objects.get(id=decoded_id)
    all_todo_lists = list(user.todolist_set.all())
    today_todolist = list(filter(lambda x: x.day == day, all_todo_lists))[0]
    tasks = list(today_todolist.task_set.all())

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

            new_task_rate = request.POST.get(f'{task_id}/rate')
            task.rate = int(new_task_rate)

            task.save()
        return redirect(f'/user_home_page/{encoded_id}')

    return render(request, 'todolist/edit_page.html',
                  {"day": today_todolist.day, "tasks": tasks, "encoded_id": encoded_id})


def add_page(request, encoded_id):
    from functions import decode
    decoded_id = decode(encoded_id)
    user = User.objects.get(id=decoded_id)
    day = get_time()
    today_todolist = ToDoList.objects.get(user=user, day=day)
    tasks = list(today_todolist.task_set.all())

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
        return redirect(f'/user_home_page/{encoded_id}')

    return render(request, 'todolist/add_page.html',
                  {"day": today_todolist.day, "tasks": tasks, "encoded_id": encoded_id})


def test(request, encoded_id):
    from functions import decode
    file_path = os.path.join(BASE_DIR, 'yahya_file')

    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        logger.critical(lines)
        days = len(lines) / 3
        logger.critical(days)
        passed_months = (days - 15) // 30
        remainder_days = (days - 15) % 30
        logger.critical(passed_months)
        logger.critical(remainder_days)
        days_dict = dict()

        t = 0
        m = 0
        for month in range(int(passed_months)):
            j = int(passed_months) * 2
            for day in range(1 + m, 31 + m):
                days_dict[f'{day - m}/{6 - passed_months + t}/23'] = [(lines[day + j + 1]),
                                                                      (lines[day + 2 + j])]
                j += 2
            t += 1

            m += 30

        m = int(passed_months) * 30
        j = 2 * int(passed_months) * 30
        for day in range(1 + m, 16 + m):
            days_dict[f'{day - m}/6/23'] = [(lines[day + j + 1]),
                                            (lines[day + 2 + j])]
            j += 2
        logger.critical(days_dict)

        decoded_id = decode(encoded_id)
        user = User.objects.get(id=decoded_id)

        for day in list(days_dict):
            try:
                todolist = ToDoList.objects.create(user=user, day=day)
                todolist.save()
                logger.critical('Todolist saved')
                for finished_task in days_dict[day][0].split(',')[1:-1]:
                    name = finished_task
                    if name == 'notion':
                        name = 'work'
                    task = Task.objects.create(todolist=todolist, name=name, bool_check=True)
                    task.save()
                    logger.critical('Task saved')

                for unfinished_task in days_dict[day][1].split(',')[1:-1]:
                    name = unfinished_task
                    if name == 'notion':
                        name = 'work'
                    task = Task.objects.create(todolist=todolist, name=name, bool_check=False)
                    task.save()
                    logger.critical('Task saved')
            except django.db.utils.IntegrityError:
                logger.critical('Task already saved')

    return home_page(request, encoded_id)

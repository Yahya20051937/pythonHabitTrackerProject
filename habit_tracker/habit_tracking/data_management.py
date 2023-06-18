from django.contrib.auth.models import User


def get_all_tasks_once(decoded_id):
    all_tasks = []

    user = User.objects.get(id=decoded_id)
    all_todo_lists = user.todolist_set.all()
    # iterate over each todolist, get all the task, append them to a list, filter the list to keep each item only once
    for todo_list in all_todo_lists:
        tasks = todo_list.task_set.all()
        for task in tasks:
            all_tasks.append(task.name)

    # now after gathering all the tasks in the list, now we should filter it
    all_tasks_once = []
    for task in all_tasks:
        if task not in all_tasks_once:
            all_tasks_once.append(task)

    return all_tasks_once



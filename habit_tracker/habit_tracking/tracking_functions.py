from django.contrib.auth.models import User


def get_habit_days_streak(all_tasks_once, habit, decoded_id):
    from .helping_function import find_indexes, sort_by_date
    from .views import logger
    # the logic behind this function is that if a habit is available in the list and checked, then we increment by one, if it is not available, we move on, if it is available but not checked, we return the days streak
    # first we have to check if the habit is already in the database at least for once
    if habit in all_tasks_once:
        days_streak = 0
        user = User.objects.get(id=decoded_id)
        all_todo_lists = list(user.todolist_set.all())
        all_todo_lists_sorted = sort_by_date(all_todo_lists, reverse=True)

        logger.critical([tdl.day for tdl in all_todo_lists_sorted])
        # this list will be sorted from the newest todolist to the oldest
        for tdl in all_todo_lists_sorted:
            tasks = tdl.task_set.all()
            logger.critical([(task.name, task.bool_check) for task in tasks])
            if habit in [task.name for task in
                         tasks]:  # if the habit is not present, then it has not been set in the todolist
                # logger.critical([task.bool_check for task in tasks if task.name == habit])
                habit_indexes = find_indexes([task.name for task in tasks], habit)
                logger.critical(habit_indexes)
                # if the habit is finished only once, then we must increment

                j = 0
                for index in habit_indexes:
                    if tasks[index].bool_check:
                        j += 1

                if j > 0:  # if true, then the task has been finished at least one time, so we must increment
                    days_streak += 1

                else:  # otherwise, we must return the days streak
                    return days_streak
            else:
                return days_streak
        return days_streak
    return None


def get_performance_in_last_n_days(decoded_id, n):
    # this function will give a percentage of performance in each day, where the total of task.rate is 100%, and we must figure then the percentage for each task.rate
    from .helping_function import sort_by_date, get_total_rate, percentage_formula
    from .views import logger
    user = User.objects.get(id=decoded_id)
    all_todo_lists = list(user.todolist_set.all())
    all_todo_lists_sorted = sort_by_date(all_todo_lists, reverse=True)

    performance_dict = dict()

    for day in range(n):
        all_tasks = all_todo_lists_sorted[day].task_set.all()
        total_rate = get_total_rate(all_tasks)
        # this list will store each task name, if it has been done or not, and its percentage rate
        tasks_data = []
        for task in all_tasks:
            task_rate_percentage = percentage_formula(total_rate, task.rate)
            tasks_data.append((task.name, task.bool_check, task_rate_percentage))
        logger.critical(tasks_data)
        performance = 0

        for task in tasks_data:
            logger.critical(task)
            if task[1] is True:    # if the task has been done, then we add to the performance the task percentage
                performance += task[2]

        # finally, the performance variable will store 100% - sum(tasks_not_finished_percentage)% in it
        logger.critical(performance)
        performance_dict[all_todo_lists_sorted[day].day] = performance

    logger.critical(performance_dict)
    return performance_dict















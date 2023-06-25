from django.contrib.auth.models import User


def get_habit_days_streak(all_tasks_once, habit, decoded_id):
    from functions import get_time
    from .helping_function import find_indexes, sort_by_date, get_days_difference
    from .views import logger
    # the logic behind this function is that if a habit is available in the list and checked, then we increment by one, if it is not available  we return the days streak, if it is available but not checked, we return the days streak
    # first we have to check if the habit is already in the database at least for once
    if habit in all_tasks_once:
        days_streak = 0
        user = User.objects.get(id=decoded_id)
        all_todo_lists = list(user.todolist_set.all())
        all_todo_lists_sorted = sort_by_date(all_todo_lists, reverse=True)

        # this list will be sorted from the newest todolist to the oldest
        # we remove the last element, to prevent getting 0 as the days streak
        for tdl in all_todo_lists_sorted[1:]:
            tasks = tdl.task_set.all()

            if habit in [task.name for task in
                         tasks]:  # if the habit is not present, then it has not been set in the todolist

                habit_indexes = find_indexes([task.name for task in tasks], habit)

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
    return 0


def get_performance_in_last_n_days(decoded_id, n):
    # this function will give a percentage of performance in each day, where the total of task.rate is 100%, and we must figure then the percentage for each task.rate
    from .helping_function import sort_by_date, get_total_rate, percentage_formula
    from database import DataBaseManagement, get_info

    from .views import logger
    user = User.objects.get(id=decoded_id)
    all_todo_lists = list(user.todolist_set.all())
    all_todo_lists_sorted = sort_by_date(all_todo_lists, reverse=True)
    logger.critical([tdl.day for tdl in all_todo_lists_sorted])
    performance_dict = dict()

    for day in range(n):
        all_tasks = all_todo_lists_sorted[day].task_set.all()

        with DataBaseManagement(decoded_id) as conn:
            for task in all_tasks:  # get the rate from the database for each task
                task.rate = get_info(conn, task.name, column='rate')

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
            if task[1] is True:  # if the task has been done, then we add to the performance the task percentage
                performance += task[2]

        # finally, the performance variable will store 100% - sum(tasks_not_finished_percentage)% in it
        logger.critical(performance)
        performance_dict[all_todo_lists_sorted[day].day] = performance

    logger.critical(performance_dict)
    return performance_dict


def track_habit(decoded_id,
                task):  # perfect (9 - 10) - very good (8 - 9) good (5 - 8) normal (5) bad (2.5 - 5) very bad (0 - 2.5)
    from .helping_function import sort_by_date
    from functions import get_time
    from .helping_function import get_days_difference
    from database import DataBaseManagement, get_info
    from .data_management import get_all_tasks_once
    from .views import logger
    user = User.objects.get(id=decoded_id)

    logger.critical(task)

    performance = 5

    all_tasks_once = get_all_tasks_once(decoded_id)

    habit_days_streak = get_habit_days_streak(all_tasks_once, task, decoded_id)
    logger.critical(habit_days_streak)

    if habit_days_streak >= 1:

        # if the days streak is bigger than one, then the performance is bigger or equal to 5
        # for each day in the days streak, we increment by a value corresponded to the value of the streak
        for i in range(habit_days_streak):
            # in the (good) range, we increment by one
            if 1 <= habit_days_streak <= 4:
                performance += 0.5

            elif 4 < habit_days_streak <= 6:
                performance += 0.25

            elif 6 < habit_days_streak <= 8:
                performance += 0.25

    else:
        with DataBaseManagement(decoded_id) as connection:
            last_time_done = get_info(connection, task)
            if last_time_done is None:  # if the habit is not stored in the database, it means that it is the first time it has been made
                return performance

            today = get_time()

            difference = get_days_difference(today, last_time_done)
            difference -= 1  # to get the difference between yesterday and the last time done
            logger.critical(difference)
            # for each day in the difference, reduce the performance
            for day in range(int(difference)):
                logger.critical(day)
                if 1 <= difference < 3:
                    performance -= 0.5

                else:
                    performance -= 0.5
                logger.critical(performance)

    return performance

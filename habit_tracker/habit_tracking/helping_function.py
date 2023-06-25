from django.contrib.auth.models import User
from functions import get_time
from .views import logger


def find_indexes(lst, element):
    indexes = []
    for i in range(len(lst)):
        if lst[i] == element:
            indexes.append(i)
    return indexes


def find_tasks(lst, element):
    tasks = []
    for i in range(len(lst)):
        if lst[i].name == element:
            tasks.append(lst[i])
    return tasks


def sort_by_date(todo_lists, reverse=False):
    from .views import logger
    sorted_list = []
    days_list = [tdl.day for tdl in todo_lists]
    # logger.critical(days_list)
    days_list = [tuple(day.split('/')) for day in days_list]
    # logger.critical(days_list)
    # the algorithm used here is to first sort the dates by list, then by month, and finally by day
    # logger.critical(len(days_list))
    days_list = sort_by_replacing(days_list, 2)
    # logger.critical(days_list)
    days_list = sort_by_replacing(days_list, 1)
    logger.critical(days_list)
    days_list = sort_by_replacing(days_list, 0)
    logger.critical(days_list)
    for day in days_list:
        day_as_a_string = f'{day[0]}/{day[1]}/{day[2]}'
        tdl = list(filter(lambda x: x.day == day_as_a_string, todo_lists))[0]
        sorted_list.append(tdl)
    if reverse:
        sorted_list.reverse()

    # logger.critical(len(sorted_list))
    # logger.critical(len(days_list))
    sorted_list = [tdl for tdl in sorted_list if get_days_difference(get_time(), tdl.day) >= 0]   # this line is used to filter the list, so as only the  lists before this day are analyzed
    return sorted_list


def sort_by_replacing(iterable, data_index):
    j = 0
    while j <= len(iterable):    # this loop is used to compare each item in the iterable with all the other items
        j += 1
        index = -1
        for date in iterable:
            index += 1
            try:
                item_to_compare = iterable[index + 1]
                condition_to_compare = False  # this variable will tell if the item should be compared with item next or not
                if data_index == 0:
                    # for example before comparing which month is older, they should be in the same year and before comparing days, they should be in the same month and in the same year!!
                    if date[data_index + 1] == item_to_compare[data_index + 1] and date[data_index + 2] == \
                            item_to_compare[
                                data_index + 2]:  # when comparing days

                        condition_to_compare = True
                elif data_index == 1:
                    if date[data_index + 1] == item_to_compare[data_index + 1]:  # when comparing months
                        condition_to_compare = True
                elif data_index == 2:
                    condition_to_compare = True  # years could always be compared !
                if condition_to_compare:
                    if int(float(item_to_compare[data_index])) < int(float(date[data_index])):
                        iterable[index] = item_to_compare
                        iterable[index + 1] = date
            except IndexError:
                pass
    # iterate over each date

    return iterable


def get_total_rate(tasks):
    total_rate = sum(task.rate for task in list(tasks))
    return total_rate


def percentage_formula(total_rate, task_rate):
    return (task_rate * 100) / total_rate


def get_todolist_length(user_id):
    user = User.objects.get(id=user_id)
    todo_lists = user.todolist_set.all()
    todolist_length = len(todo_lists)
    return todolist_length


def get_days_difference(date1, date2):
    logger.critical(f'{date1}, {date2}')
    difference = 0
    # first we calculate the years difference, and we multiply it by 365
    year1 = float(date1.split('/')[2])
    year2 = float(date2.split('/')[2])

    difference += (year1 - year2) * 365

    # then we calculate the month difference and multiply it by 30

    month1 = float(date1.split('/')[1])
    month2 = float(date2.split('/')[1])

    difference += (month1 - month2) * 30

    # then lastly, we calculate the day difference

    day1 = float(date1.split('/')[0])
    day2 = float(date2.split('/')[0])

    difference += day1 - day2

    return difference

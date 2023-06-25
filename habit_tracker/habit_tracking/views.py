import logging
import numpy
import os
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg
from io import BytesIO
import base64
from django.shortcuts import render
from functions import get_time

from .data_management import get_all_tasks_once, User
from .tracking_functions import get_habit_days_streak, get_performance_in_last_n_days

BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(format='%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d] %(message)s', datefmt='%d-%m-%Y '
                                                                                                       '%H:%M:%S ',
                    level=logging.CRITICAL,
                    filename='logs.txt')
logger = logging.getLogger('habit_tracking')


# Create your views here.
def tracking_home_page(request, encoded_id):
    time = get_time(for_url=True)
    return render(request, 'habit_tracking/tracking_home.html', {'encoded_id': encoded_id, 'time': time})


def get_habit_days_streak_view(request, encoded_id):
    from functions import decode
    decoded_id = decode(encoded_id)
    all_tasks_once = get_all_tasks_once(decoded_id=decoded_id)
    if request.method == 'POST':
        selected_task = request.POST.get("selected_task")
        habit_days_streak = get_habit_days_streak(all_tasks_once, selected_task, decoded_id)
        return render(request, 'habit_tracking/habits_days_streak.html',
                      {"encoded_id": encoded_id, "task": selected_task, "days_streak": habit_days_streak,
                       "display": True})
    return render(request, 'habit_tracking/habits_days_streak.html',
                  {"encoded_id": encoded_id, "all_tasks": all_tasks_once, "display": False})


def get_performance_graph_view(request, encoded_id):
    from functions import decode
    from .helping_function import get_todolist_length
    decoded_id = decode(encoded_id)
    todo_lists_length = get_todolist_length(decoded_id)
    logger.critical(todo_lists_length)
    if request.method == 'POST':
        selected_n = request.POST.get("selected_n")
        graph_coordinates = get_performance_in_last_n_days(decoded_id, int(selected_n))
        x_coordinates = numpy.array(range(len(list(graph_coordinates.values()))))
        y_coordinates = numpy.array(list(graph_coordinates.values()))
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x_coordinates, y_coordinates)
        # code provided by CHAT-GPT to display the graph in the html page along with a toolbar
        canvas = FigureCanvasTkAgg(fig)
        toolbar = NavigationToolbar2Tk(canvas, None)
        buffer = BytesIO()
        canvas.print_png(buffer)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        context = {"image_base64": image_base64, "display": True, "encoded_id": encoded_id, "tool_bar": toolbar}
        return render(request, 'habit_tracking/habit_performance.html', context)
    return render(request, 'habit_tracking/habit_performance.html',
                  {'display': False, 'numbers': range(1, todo_lists_length + 1), "encoded_id": encoded_id})

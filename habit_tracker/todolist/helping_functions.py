import matplotlib.pyplot as plt


def modify_performance(decoded_id, tasks):
    from habit_tracking.tracking_functions import track_habit
    from .views import logger

    for task in tasks:
        performance = track_habit(decoded_id, task.name)
        logger.critical(f'{task.name}, {performance}')

        if performance > 10:
            task.performance = 'perfect'
        elif performance > 8:
            task.performance = 'vert_good'
        elif performance > 6:
            task.performance = 'good'
        elif performance > 4:
            task.performance = 'normal'
        elif performance > 2:
            task.performance = 'bad'
        else:
            task.performance = 'very_bad'

        logger.critical(f'{task.name}, {task.performance}')


def get_style_tag():  # code provide by CHAT-GPT
    color_mapping = {
        'Perfect': 'rgb(0, 0, 255)',  # Blue
        'Very_Good': 'rgb(51, 153, 255)',  # Light Blue
        'Good': 'rgb(204, 204, 204)',  # Light Gray
        'Normal': 'rgb(255, 255, 255)',  # White
        'Bad': 'rgb(255, 153, 153)',  # Light Red
        'Very_Bad': 'rgb(255, 51, 51)'  # Red
    }

    css_rules = ''
    for class_name, color in color_mapping.items():
        css_rules += f'th.{class_name} {{color: {color};}}\n'

    style_tag = f'{css_rules}'
    return style_tag


def transform_underscore_to_slash(string):
    transformed_string = string.replace('_', '/')
    return transformed_string


def transform_slash_to_underscore(string):
    transformed_string = string.replace('/', '_')
    return transformed_string


def get_day_from_request(request):
    day = request.POST.get('day')
    month = request.POST.get('month')
    year = request.POST.get("year")

    # this is statement is to correct the day number
    if day == '31' and month not in ['1', '3', '5', '7', '8', '10', '12']:
        day = '30'

    if day > '28' and month == '2':
        day = '28'

    date = f'{day}_{month}_{year}'
    return date


def handle_performance_color(performance):
    if performance == 100:
        color = 'blue'
    elif performance > 80:
        color = 'lightblue'
    elif performance > 60:
        color = 'limegreen'
    elif performance > 40:
        color = 'white'
    elif performance > 20:
        color = 'red'
    else:
        color = 'black'

    return color


def get_image_base64(day_performance):
    import numpy as np
    import base64
    from io import BytesIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    category = ['Performance']
    value = [day_performance]

    fig, ax = plt.subplots(figsize=(2, 10))
    color = handle_performance_color(day_performance)
    ax.bar(category, value, color=color)
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], minor=False)

    # ax.tick_params(axis='x', rotation=90)
    # ax.tick_params(axis='y', rotation=90)

    buffer = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)
    buffer.seek(0)

    image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image

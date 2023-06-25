def modify_performance(decoded_id, tasks):
    from habit_tracking.tracking_functions import track_habit
    from .views import logger

    for task in tasks:
        performance = track_habit(decoded_id, task.name)
        logger.critical(f'{task.name}, {performance}')

        if performance >= 10:
            task.performance = 'perfect'
        elif performance >= 8:
            task.performance = 'vert_good'
        elif performance >= 6:
            task.performance = 'good'
        elif performance >= 4:
            task.performance = 'normal'
        elif performance >= 2:
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

    date =  f'{day}_{month}_{year}'
    return date

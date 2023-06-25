from django import template
from database import DataBaseManagement, get_info

register = template.Library()


@register.filter
def extract_starting_time(value):
    if value:
        return value.split('-')[0]
    return value

# code provided by CHAT-GPT


@register.filter
def extract_ending_time(value):
    if value:
        return value.split('-')[1]
    return value


@register.filter
def extract_day(value):
    if value:
        return value.split('_')[0]


@register.filter
def extract_month(value):
    if value:
        return value.split('_')[1]


@register.filter
def extract_year(value):
    if value:
        return value.split('_')[2]


@register.filter
def extract_rate(task, decoded_id):
    with DataBaseManagement(decoded_id) as conn:
        rate = get_info(conn, task.name, 'rate')
        return rate
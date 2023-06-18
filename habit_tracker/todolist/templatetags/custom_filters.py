from django import template

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
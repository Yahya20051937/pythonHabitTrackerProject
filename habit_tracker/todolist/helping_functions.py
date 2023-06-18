import time


def get_time():
    current_time = time.localtime()
    current_date = f'{current_time.tm_mday}/{current_time.tm_mon}/{str(current_time.tm_year)[2:]}'
    return current_date

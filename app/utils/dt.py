"""日期时间处理
"""

__all__ = [
    'DATE_SEPARATOR', 'TIME_SEPARATOR', 'DATETIME_SEPARATOR',
    'DATE_FORMATTER', 'TIME_FORMATTER', 'DATETIME_FORMATTER',
    'CLOCK_FORMATTER', 'TIMESTAMP_FORMATTER',
    'is_date_str', 'is_time_str', 'is_datetime_str',
    'date_str_2_datetime', 'time_str_2_datetime', 'datetime_str_2_datetime',
    'second_start', 'minute_start', 'hour_start', 'day_start',
    'week_start', 'month_start', 'month_end'
]

import re
from datetime import datetime, timedelta

DATE_SEPARATOR = '-'
TIME_SEPARATOR = ':'
DATETIME_SEPARATOR = ' '
DATE_FORMATTER = '%Y-%m-%d'
TIME_FORMATTER = '%H:%M:%S'
DATETIME_FORMATTER = '%Y-%m-%d %H:%M:%S'
CLOCK_FORMATTER = '%H:00:00'
TIMESTAMP_FORMATTER = '%Y%m%d_%H%M%S_%f'


def is_date_str(date_str):
    date_str = str(date_str)
    if not re.match(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$', date_str):
        return False
    year, month, day = list(map(int, date_str.split(DATE_SEPARATOR)))
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return False if day > 31 else True
    elif month in [4, 6, 9, 11]:
        return False if day > 30 else True
    else:
        if year % 400 != 0 and year % 4 == 0:
            return False if day > 29 else True
        else:
            return False if day > 28 else True
    return False


def is_time_str(time_str):
    time_str = str(time_str)
    if re.match(r'^([0-1][0-9]|2[0-3])(:[0-5][0-9]){2}$', time_str):
        return True
    return False


def is_datetime_str(datetime_str):
    datetime_str = str(datetime_str)
    date_str, time_str = datetime_str.split(DATETIME_SEPARATOR)
    return is_date_str(date_str) and is_time_str(time_str)


def date_str_2_datetime(date_str):
    if is_date_str(date_str):
        return datetime.strptime(date_str, DATE_FORMATTER)
    return None


def time_str_2_datetime(time_str, dt=datetime.now()):
    if is_time_str(time_str):
        hour, minute, second = list(map(int, time_str.split(TIME_SEPARATOR)))
        return datetime(dt.year, dt.month, dt.day, hour, minute, second)
    return None


def datetime_str_2_datetime(datetime_str):
    if is_datetime_str(datetime_str):
        return datetime.strptime(datetime_str, DATETIME_FORMATTER)
    return None


def second_start(dt):
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return None


def minute_start(dt):
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    return None


def hour_start(dt):
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour)
    return None


def day_start(dt):
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day)
    return None


def week_start(dt):
    while dt.weekday() > 0:
        dt -= timedelta(days=1)
    return day_start(dt)


def month_start(dt):
    return datetime(dt.year, dt.month, 1)


def month_end(dt):
    month = dt.month
    while dt.month == month:
        dt += timedelta(days=1)
    return day_start(dt - timedelta(days=1))

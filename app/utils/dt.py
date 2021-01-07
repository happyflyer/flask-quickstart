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
    """Examples:
        >>> is_date_str('2020-02-29')
        True
        >>> is_date_str('2019-02-29')
        False
    """
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
    """Examples:
        >>> is_time_str('23:59:59')
        True
        >>> is_time_str('23:59:60')
        False
    """
    time_str = str(time_str)
    if re.match(r'^([0-1][0-9]|2[0-3])(:[0-5][0-9]){2}$', time_str):
        return True
    return False


def is_datetime_str(datetime_str):
    """Examples:
        >>> is_datetime_str('2020-02-29 23:59:59')
        True
        >>> is_datetime_str('2020-02-29 23:59:60')
        False
    """
    datetime_str = str(datetime_str)
    date_str, time_str = datetime_str.split(DATETIME_SEPARATOR)
    return is_date_str(date_str) and is_time_str(time_str)


def date_str_2_datetime(date_str):
    """Examples:
        >>> date_str_2_datetime('2020-02-29')
        datetime.datetime(2020, 2, 29, 0, 0)
        >>> date_str_2_datetime('2019-02-29')
    """
    if is_date_str(date_str):
        return datetime.strptime(date_str, DATE_FORMATTER)
    return None


def time_str_2_datetime(time_str, dt=datetime.now()):
    """Examples:
        >>> time_str_2_datetime('23:59:59', dt=date_str_2_datetime('2020-02-29'))
        datetime.datetime(2020, 2, 29, 23, 59, 59)
    """
    if is_time_str(time_str):
        hour, minute, second = list(map(int, time_str.split(TIME_SEPARATOR)))
        return datetime(dt.year, dt.month, dt.day, hour, minute, second)
    return None


def datetime_str_2_datetime(datetime_str):
    """Examples:
        >>> datetime_str_2_datetime('2020-02-29 23:59:59')
        datetime.datetime(2020, 2, 29, 23, 59, 59)
    """
    if is_datetime_str(datetime_str):
        return datetime.strptime(datetime_str, DATETIME_FORMATTER)
    return None


def second_start(dt):
    """Examples:
        >>> second_start(datetime_str_2_datetime('2020-02-29 23:59:59'))
        datetime.datetime(2020, 2, 29, 23, 59, 59)
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return None


def minute_start(dt):
    """Examples:
        >>> minute_start(datetime_str_2_datetime('2020-02-29 23:59:59'))
        datetime.datetime(2020, 2, 29, 23, 59)
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    return None


def hour_start(dt):
    """Examples:
        >>> hour_start(datetime_str_2_datetime('2020-02-29 23:59:59'))
        datetime.datetime(2020, 2, 29, 23, 0)
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour)
    return None


def day_start(dt):
    """Examples:
        >>> day_start(datetime_str_2_datetime('2020-02-29 23:59:59'))
        datetime.datetime(2020, 2, 29, 0, 0)
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day)
    return None


def week_start(dt):
    """Examples:
        >>> week_start(datetime_str_2_datetime('2020-02-29 23:59:59'))
        datetime.datetime(2020, 2, 24, 0, 0)
    """
    while dt.weekday() > 0:
        dt -= timedelta(days=1)
    return day_start(dt)


def month_start(dt):
    """Examples:
        >>> month_start(datetime_str_2_datetime('2020-02-29 23:59:59'))
        datetime.datetime(2020, 2, 1, 0, 0)
    """
    return datetime(dt.year, dt.month, 1)


def month_end(dt):
    """Examples:
        >>> month_end(datetime_str_2_datetime('2020-02-29 23:59:59'))
        datetime.datetime(2020, 2, 29, 0, 0)
    """
    month = dt.month
    while dt.month == month:
        dt += timedelta(days=1)
    return day_start(dt - timedelta(days=1))

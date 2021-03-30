"""日期时间处理
"""

__all__ = [
    'DATE_SEPARATOR',
    'TIME_SEPARATOR',
    'DATETIME_SEPARATOR',
    'DATE_FORMATTER',
    'TIME_FORMATTER',
    'DATETIME_FORMATTER',
    'CLOCK_FORMATTER',
    'TIMESTAMP_FORMATTER',
    'is_date_str',
    'is_time_str',
    'is_datetime_str',
    'date_str_2_datetime',
    'time_str_2_datetime',
    'datetime_str_2_datetime',
    'datetime_format',
    'second_start', 'second_end',
    'minute_start', 'minute_end',
    'hour_start', 'hour_end',
    'day_start', 'day_end',
    'week_start', 'week_end',
    'month_start', 'month_end'
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


def is_date_str(d: str) -> bool:
    """判断是否为日期字符串
    """
    d = str(d)
    if not re.match(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$', d):
        return False
    year, month, day = list(map(int, d.split(DATE_SEPARATOR)))
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return False if day > 31 else True
    elif month in [4, 6, 9, 11]:
        return False if day > 30 else True
    else:
        if year % 400 != 0 and year % 4 == 0:
            return False if day > 29 else True
        else:
            return False if day > 28 else True


def is_time_str(t: str) -> bool:
    """判断是否为时间字符串
    """
    t = str(t)
    if re.match(r'^([0-1][0-9]|2[0-3])(:[0-5][0-9]){2}$', t):
        return True
    return False


def is_datetime_str(dt: str) -> bool:
    """判断是否为日期时间字符串
    """
    dt = str(dt)
    date_str, time_str = dt.split(DATETIME_SEPARATOR)
    return is_date_str(date_str) and is_time_str(time_str)


def date_str_2_datetime(d: str) -> datetime:
    """日期字符串转日期时间
    """
    if is_date_str(d):
        return datetime.strptime(d, DATE_FORMATTER)
    return None


def time_str_2_datetime(t: str, dt=datetime.now()) -> datetime:
    """时间字符串转日期时间
    """
    if is_time_str(t):
        hour, minute, second = list(map(int, t.split(TIME_SEPARATOR)))
        return datetime(dt.year, dt.month, dt.day, hour, minute, second)
    return None


def datetime_str_2_datetime(dt: str) -> datetime:
    """日期时间字符串转日期时间
    """
    if is_datetime_str(dt):
        return datetime.strptime(dt, DATETIME_FORMATTER)
    return None


def datetime_format(dt: datetime, formatter=DATETIME_FORMATTER) -> str:
    """日期时间格式化为字符串
    """
    if isinstance(dt, datetime):
        return dt.strftime(formatter)
    return None


def second_start(dt: datetime) -> datetime:
    """日期时间秒开始
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return None


def second_end(dt: datetime) -> datetime:
    """日期时间秒结束
    """
    start = second_start(dt)
    if start:
        return start + timedelta(seconds=1, microseconds=-1)
    return None


def minute_start(dt: datetime) -> datetime:
    """日期时间分钟开始
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    return None


def minute_end(dt: datetime) -> datetime:
    """日期时间分钟结束
    """
    start = minute_start(dt)
    if start:
        return start + timedelta(minutes=1, microseconds=-1)
    return None


def hour_start(dt: datetime) -> datetime:
    """日期时间小时开始
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day, dt.hour)
    return None


def hour_end(dt: datetime) -> datetime:
    """日期时间小时结束
    """
    start = hour_start(dt)
    if start:
        return start + timedelta(hours=1, microseconds=-1)
    return None


def day_start(dt: datetime) -> datetime:
    """日期时间天开始
    """
    if isinstance(dt, datetime):
        return datetime(dt.year, dt.month, dt.day)
    return None


def day_end(dt: datetime) -> datetime:
    """日期时间天结束
    """
    start = day_start(dt)
    if start:
        return start + timedelta(days=1, microseconds=-1)
    return None


def week_start(dt: datetime) -> datetime:
    """日期时间周开始
    """
    while dt.weekday() > 0:
        dt -= timedelta(days=1)
    return day_start(dt)


def week_end(dt: datetime) -> datetime:
    """日期时间周结束
    """
    start = week_start(dt)
    if start:
        return start + timedelta(weeks=1, microseconds=-1)
    return None


def month_start(dt: datetime) -> datetime:
    """日期时间月开始
    """
    return datetime(dt.year, dt.month, 1)


def month_end(dt: datetime) -> datetime:
    """日期时间月结束
    """
    month = dt.month
    while dt.month == month:
        dt += timedelta(days=1)
    return day_start(dt - timedelta(days=1))

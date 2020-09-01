# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta


# 日期
DATE_SEPARATOR = '-'
DATE_FORMATTER = DATE_SEPARATOR.join(['%Y', '%m', '%d'])
# 时间
TIME_SEPARATOR = ':'
TIME_FORMATTER = TIME_SEPARATOR.join(['%H', '%M', '%S'])
CLOCK_FORMATTER = TIME_SEPARATOR.join(['%H', '00', '00'])
# 日期时间
DATETIME_SEPARATOR = ' '
DATETIME_FORMATTER = DATETIME_SEPARATOR.join([DATE_FORMATTER, TIME_FORMATTER])


def is_date_str(date_str):
    """判断是否为合法的日期字符串

    Args:
        date_str (str): 日期字符串，形如：'YYYY-mm-dd'

    Returns:
        bool: 检查结果
    """
    date_str = str(date_str)
    if not re.match(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$', date_str):
        return False
    year, month, day = list(map(int, str.split(date_str, DATE_SEPARATOR)))
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return False if day > 31 else True
    elif month in [4, 6, 9, 11]:
        return False if day > 30 else True
    else:
        if year % 400 != 0 and year % 4 == 0:
            return False if day > 29 else True
        else:
            return False if day > 28 else True
    return True


def is_time_str(time_str):
    """检查是否为合法的时间字符串

    Args:
        time_str (str): 时间字符串，形如：'hh:MM:ss'

    Returns:
        bool: 检查结果
    """
    time_str = str(time_str)
    if re.match(r'^([0-1][0-9]|2[0-3])(:[0-5][0-9]){2}$', time_str):
        return True
    return False


def date_str_2_dt(date_str):
    """日期字符串转 datetime 类型

    Args:
        date_str (str): 日期字符串，形如：'YYYY-mm-dd'

    Returns:
        datetime: 转换结果，当日期字符串不合法时返回None
    """
    if not is_date_str(date_str):
        return None
    return datetime.strptime(date_str, DATE_FORMATTER)


def time_str_2_dt(time_str, dt=datetime.now()):
    """时间字符串转 datetime 类型

    Args:
        time_str (str): 时间字符串，形如：'HH:MM:SS'
        dt (datetime), optional): 转换后的日期. Defaults to datetime.now().

    Returns:
        datetime: 转换结果，当时间字符串不合法时返回None
    """
    if not is_time_str(time_str):
        return None
    hour, minute, second = list(map(int, str.split(time_str, TIME_SEPARATOR)))
    return datetime(dt.year, dt.month, dt.day, hour, minute, second)


def dt_str_2_dt(dt_str):
    """日期时间字符串转 datetime 类型

    Args:
        dt_str (str): 日期时间字符串，形如：'YYYY-mm-dd HH:MM:SS'

    Returns:
        datetime: 转换结果，当日期时间字符串不可用时返回None
    """
    dt_str = str(dt_str)
    date_str, time_str = str.split(dt_str, DATETIME_SEPARATOR)
    if not (is_date_str(date_str) and is_time_str(time_str)):
        return None
    return datetime.strptime(dt_str, DATETIME_FORMATTER)


def second_start(dt):
    """设置 datetime 为整数秒

    Args:
        dt (datetime): datetime

    Returns:
        datetime: 转换结果
    """
    if not isinstance(dt, datetime):
        return None
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def minute_start(dt):
    """设置 datetime 为整数分钟

    Args:
        dt (datetime): datetime

    Returns:
        datetime: 转换结果
    """
    if not isinstance(dt, datetime):
        return None
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)


def hour_start(dt):
    """设置 datetime 为整数小时

    Args:
        dt (datetime): datetime

    Returns:
        datetime: 转换结果
    """
    if not isinstance(dt, datetime):
        return None
    return datetime(dt.year, dt.month, dt.day, dt.hour)


def day_start(dt):
    """设置 datetime 为当天的00:00:00

    Args:
        dt (datetime): datetime

    Returns:
        datetime: 转换结果
    """
    if not isinstance(dt, datetime):
        return None
    return datetime(dt.year, dt.month, dt.day)


def week_start(dt):
    """设置 datetime 为当前周星期一的00:00:00

    Args:
        dt (datetime): datetime

    Returns:
        datetime: 转换结果
    """
    while dt.weekday() > 0:
        dt -= timedelta(days=1)
    return day_start(dt)


def month_start(dt):
    """设置 datetime 为当月周第一天的00:00:00

    Args:
        dt (datetime): datetime

    Returns:
        datetime: 转换结果
    """
    return datetime(dt.year, dt.month, 1)


def month_end(dt):
    """设置 datetime 为当月周最后一天的00:00:00

    Args:
        dt (datetime): datetime

    Returns:
        datetime: 转换结果
    """
    month = dt.month
    while dt.month == month:
        dt += timedelta(days=1)
    return day_start(dt - timedelta(days=1))

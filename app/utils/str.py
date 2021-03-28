"""字符串处理
"""

__all__ = ['has_empty', 'all_empty', 'is_empty']

from typing import Any


_empty = ''


def has_empty(*values) -> bool:
    """values中是否存在空字符串，如果values中含有非str类型对象将抛出TypeError
    """
    for value in values:
        if isinstance(value, str):
            if value.strip() == _empty:
                return True
        else:
            raise TypeError("not str")
    return False


def all_empty(*values) -> bool:
    """values中是否都是空字符串，如果values中含有非str类型对象将抛出TypeError
    """
    for value in values:
        if isinstance(value, str):
            if value.strip() != _empty:
                return False
        else:
            raise TypeError("not str")
    return True


def is_empty(value: Any) -> bool:
    """value是否为空字符串，value为int类型时均为非空
    """
    if isinstance(value, int):
        return False
    if isinstance(value, str):
        return value.strip() == _empty
    return False if value else True

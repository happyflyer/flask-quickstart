# -*- coding: utf-8 -*-

from . import EMPTY


__all__ = [
    'has_empty',
    'all_empty'
]


def has_empty(*values):
    """是否存在空字符串\n
    Args:\n
        values list
    Returns:\n
        True or False
    Demo:\n
        >>> has_empty('hh', 'kk')
        False
        >>> has_empty('hh', 'kk', '   ')
        True
    """
    for v in values:
        # 有一个元素为空就返回有空
        if v is None or str.strip(v) == EMPTY:
            return True
    return False


def all_empty(*values):
    """是否都是空字符串\n
    Args:\n
        values list
    Returns:\n
        True or False
    Demo:\n
        >>> all_empty('hh', 'kk', '   ')
        False
        >>> all_empty('  ', '', '   ')
        True
    """
    for v in values:
        if v is not None and str.strip(v) != EMPTY:
            return False
    # 所有元素都为空才返回为空
    return True

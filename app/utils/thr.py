# -*- coding: utf-8 -*-

from threading import Thread


__all__ = [
    'async_execute',
    'parallel_execute'
]


def async_execute(f):
    """新开一个子线程执行函数\n
    Args:\n
        f function
    """
    def decorated_view(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setDaemon(True)
        thr.start()
    decorated_view.__name__ = f.__name__
    decorated_view.__doc__ = f.__doc__
    return decorated_view


def parallel_execute(threads=10):
    """使用并行子线程执行函数\n
    Args:\n
        threads int 并行执行的子线程数
    """
    def parallel_decorator(f):
        def decorated_view(*args, **kwargs):
            for i in range(threads):
                thr = Thread(target=f, args=args, kwargs=kwargs)
                thr.setDaemon(True)
                thr.start()
        decorated_view.__name__ = f.__name__
        decorated_view.__doc__ = f.__doc__
        return decorated_view
    return parallel_decorator

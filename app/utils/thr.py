# -*- coding: utf-8 -*-

from threading import Thread


def async_execute(f):
    """新开一个线程里执行函数

    Args:
        f (function): 函数

    Returns:
        function: 装饰器
    """
    def decorator(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setDaemon(True)
        thr.start()
    decorator.__name__ = f.__name__
    decorator.__doc__ = f.__doc__
    return decorator


def parallel_execute(threads=10):
    """使用并行子线程执行函数

    Args:
        threads (int, optional): 并行线程数. Defaults to 10.

    Returns:
        function: 装饰器
    """
    def decorator(f):
        def decorator2(*args, **kwargs):
            for i in range(threads):
                thr = Thread(target=f, args=args, kwargs=kwargs)
                thr.setDaemon(True)
                thr.start()
        decorator2.__name__ = f.__name__
        decorator2.__doc__ = f.__doc__
        return decorator2
    return decorator

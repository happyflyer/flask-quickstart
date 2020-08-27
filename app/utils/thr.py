# -*- coding: utf-8 -*-

from threading import Thread


def async_execute(f):
    """新开一个子线程执行函数\n
    Args:\n
        f function
    """
    def decorator(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setDaemon(True)
        thr.start()
    decorator.__name__ = f.__name__
    decorator.__doc__ = f.__doc__
    return decorator


def parallel_execute(threads=10):
    """使用并行子线程执行函数\n
    Args:\n
        threads int 并行执行的子线程数
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

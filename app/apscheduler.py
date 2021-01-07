"""解决多进程中APScheduler重复运行的问题
https://ld246.com/article/1582878621206
"""

import atexit
import fcntl


def init_apscheduler(app, scheduler):
    f = open('data/scheduler.lock', 'wb')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
    atexit.register(unlock)

"""设置定时任务
"""

from . import scheduler


def do_jobs():
    scheduler.remove_all_jobs()

"""文本文件读写
"""

__all__ = ['read_json', 'write_json']

import os
import json
from threading import Thread, Lock

_encoding = 'utf-8'
_indent = 2
_mutex = Lock()


def read_json(filename: str) -> dict:
    """读json
    """
    payload = {}
    if not os.path.exists(filename):
        return payload
    _mutex.acquire(10)
    with open(filename, 'r', encoding=_encoding) as filename:
        payload = json.load(filename)
    _mutex.release()
    return payload


def write_json(payload: dict, filename: str, new_thread=True) -> None:
    """写json
    """
    if new_thread:
        thr = Thread(target=_write_json, args=(payload, filename))
        thr.start()
    else:
        _write_json(payload, filename)


def _write_json(payload: dict, filename: str) -> None:
    filedir = os.path.abspath(os.path.dirname(filename))
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    _mutex.acquire(10)
    with open(filename, 'w', encoding=_encoding) as f:
        json.dump(payload, f, indent=_indent)
    _mutex.release()

"""json读写
"""

__all__ = [
    'read_json', 'write_json'
]

import os
import json
from threading import Thread, Lock

_empty = ''
_encoding = 'utf-8'
_indent = 2
mutex = Lock()


def read_json(filename):
    payload = {}
    if not os.path.exists(filename):
        return payload
    mutex.acquire(10)
    with open(filename, 'r', encoding=_encoding) as f:
        payload = json.load(f)
    mutex.release()
    return payload


def write_json(payload, filename, new_thread=True):
    if new_thread:
        thr = Thread(target=_write_json, args=(payload, filename))
        thr.start()
    else:
        _write_json(payload, filename)


def _write_json(payload, filename):
    filedir = os.path.abspath(os.path.dirname(filename))
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    mutex.acquire(10)
    with open(filename, 'w', encoding=_encoding) as f:
        json.dump(payload, f, indent=_indent)
    mutex.release()

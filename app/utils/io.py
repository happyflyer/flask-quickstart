# -*- coding: utf-8 -*-

import os
import json
from threading import Thread

from . import EMPTY, ENCODING


# json文件缩进空格
JSON_INDENT = 2


def read_json(filename):
    """读取json

    Args:
        filename (str): 文件路径

    Returns:
        dict: 文件内容，当文件不可用时返回 {}
    """
    payload = {}
    if not os.path.exists(filename):
        return payload
    with open(filename, 'r', encoding=ENCODING) as f:
        payload = json.load(f)
    return payload


def write_json(payload, filename, new_thread=False):
    """写json

    Args:
        payload (dict): 文件内容
        filename (str): 文件路径
        new_thread (bool, optional): 是否使用新线程. Defaults to False.
    """
    if new_thread:
        thr = Thread(target=_write_json, args=(payload, filename), daemon=True)
        thr.start()
    else:
        _write_json(payload, filename)


def _write_json(payload, filename):
    filedir = os.path.abspath(os.path.dirname(filename))
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    with open(filename, 'w', encoding=ENCODING) as f:
        json.dump(payload, f, indent=JSON_INDENT)


def read_properties(filename):
    """读取properties

    Args:
        filename (str): 文件路径

    Returns:
        dict: 文件内容，当文件不可用时返回 {}
    """
    properties = []
    with open(filename, 'r', encoding=ENCODING) as f:
        for line in f.readlines():
            line = line.strip().replace('\n', '')
            # 去掉注释
            if line.find("#") != -1:
                line = line[:line.find('#')]
            if line.strip() != EMPTY:
                properties.append(line.strip())

    def properties_2_dict(properties):
        payload = {}

        def parse(current_dict, left, right):
            if left.find('.') != -1:
                # 如果找到分隔符，就继续向里解析
                prefix = left.split('.')[0]
                not_prefix = left[len(prefix)+1:]
                if prefix not in current_dict:
                    current_dict.setdefault(prefix, {})
                parse(current_dict[prefix], not_prefix, right)
            else:
                current_dict[left] = right
        for line in properties:
            if line.find('=') > 0 and line.count('=') == 1:
                left, right = line.split('=')
                parse(payload, left, right)
        return payload
    return properties_2_dict(properties)

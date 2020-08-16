# -*- coding: utf-8 -*-

import os
import json
from threading import Thread

from . import EMPTY, ENCODING


__all__ = [
    'JSON_INDENT',
    'read_json',
    'write_json',
    'read_properties'
]

# json文件缩进空格
JSON_INDENT = 2


def read_json(filename):
    """读取json文件\n
    Args:\n
        filename str 文件路径
    Returns:\n
        payload dict json文件内容，当文件路径不可用时，返回{}
    Demo:\n
        >>> read_json('demo.json')
    """
    payload = {}
    if not os.path.exists(filename):
        return payload
    with open(filename, 'r', encoding=ENCODING) as f:
        payload = json.load(f)
    return payload


def write_json(payload, filename, new_thread=False):
    """将payload写入到json文件\n
    Args:\n
        payload dict 数据
        filename str 文件路径
        new_thread bool 是否开一个子线程写文件
    Demo:\n
        >>> write_json({'k': 'v'}, 'demo.json')
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
    """读取properties文件\n
    Args:\n
        filename str 文件路径
    Returns:\n
        payload dict 文件内容，当文件路径不可用时，返回{}
    Demo:\n
        >>> read_properties('demo.properties')
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

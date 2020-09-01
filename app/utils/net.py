# -*- coding: utf-8 -*-

import platform
import re
import subprocess
from queue import Queue

import psutil

from . import ENCODING
from .thr import parallel_execute


# 本地回环地址
LOOPBACK_IP_ADDRESS = '127.0.0.1'
# ping 次数
PING_COUNT = 1
# ping 超时时间
PING_TIMEOUT = 1


def get_os():
    """获得操作系统名

    Returns:
        str: 'Windows'|'Linux'|'Darwin'
    """
    return platform.system()


def get_ip(filter_prefix=None):
    """获得本机ip

    Args:
        filter_prefix (str, optional): 过滤前缀. Defaults to None.

    Returns:
        list: 本机ip

    Examples:
        >>> get_ip()
        >>> get_ip('192.168.1.')
    """
    ip_address_list = []
    dic = psutil.net_if_addrs()
    for adapter in dic:
        snicList = dic[adapter]
        for snic in snicList:
            if snic.family.name == 'AF_INET':
                ip_address_list.append(snic.address)
    # 排除本地回环地址
    ip_address_list = list(filter(lambda x: x != LOOPBACK_IP_ADDRESS, ip_address_list))
    # 通过前缀筛选
    if filter_prefix:
        ip_address_list = list(filter(lambda x: x.startswith(filter_prefix), ip_address_list))
    return ip_address_list


def check_ip(ip_address):
    """检查ip地址格式

    Args:
        ip_address (str)): ip地址

    Returns:
        bool: 检查结果
    """
    pattern = r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$'
    if re.match(pattern, ip_address):
        return True
    return False


def extract_ip(text):
    """提取ip地址

    Args:
        text (str): 文本

    Returns:
        str: 文本中首次出现的ip地址，当文本中不包含ip地址时返回None
    """
    pattern = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
    match_obj = re.search(pattern, text)
    if match_obj:
        return match_obj.group()
    return None


def ping_ip(ip_address):
    """ping ip

    Args:
        ip_address (str): ip地址

    Returns:
        bool: 是否ping通

    Examples:
        >>> ping_ip('192.168.1.1')
    """
    # 如果格式不正确，直接返回 False
    if not check_ip(ip_address):
        return False
    if get_os() == 'Windows':
        count = '-n'
        timeout = '-w'
    elif get_os() == 'Linux':
        count = '-c'
        timeout = '-W'
    elif get_os() == 'Darwin':
        count = '-c'
        timeout = '-t'
    else:
        return False
    ret = subprocess.run(['ping', count, str(PING_COUNT), timeout, str(PING_TIMEOUT), ip_address],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # NOQA
    return ret.returncode == 0


def scan_ip(ip_address, start=1, end=255, including_me=False):
    """扫描局域网下的ip地址

    Args:
        ip_address (str): ip地址，用于获取网段
        start (int, optional): 开始数. Defaults to 1.
        end (int, optional): 结束数，包括. Defaults to 255.
        including_me (bool, optional): 是否包含提供的ip地址. Defaults to False.

    Returns:
        list: 局域网下可以ping通的ip地址，当局域网不可用时返回 []

    Examples:
        >>> scan_ip(get_ip('192.168.1.1')[0])
    """
    # 如果格式不正确，直接返回 []
    ip_address_list = []
    if not check_ip(ip_address):
        return ip_address_list
    ip_prefix = ip_address.split('.')[:-1]
    q = Queue()
    for i in range(start, end + 1):
        q.put('.'.join(ip_prefix + [str(i)]))
    _ping_fun(q, ip_address_list)
    q.join()
    # 排除本身
    if not including_me:
        ip_address_list = list(filter(lambda x: x != ip_address, ip_address_list))
    # 排序
    ip_address_list.sort(key=lambda x: int(x.split('.')[-1]))
    return ip_address_list


@parallel_execute(128)
def _ping_fun(in_queue, out_list):
    while not in_queue.empty():
        ip = in_queue.get()
        if ping_ip(ip):
            out_list.append(ip)
        in_queue.task_done()

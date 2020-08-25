# -*- coding: utf-8 -*-

import os
import re
from queue import Queue

import cv2

from .cv import save_screenshot
from .net import check_ip, extract_ip, scan_ip
from .thr import parallel_execute


# rtsp视频流默认端口
RTSP_PORT = 554


def check_rtsp(rtsp_url):
    """检查rtsp_url格式\n
    Args:\n
        rtsp_url: str
    Returns:\n
        True or False
    """
    protocol = re.split('://', rtsp_url)[0]
    if protocol != 'rtsp':
        return False
    pattern = r'^rtsp://([\S]*:[\S]*@)?((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}[\S]*'
    if re.match(pattern, rtsp_url):
        return True
    return False


def scan_rtsp(ip_address, user=None, pwd=None, port=None):
    """扫描局域网下的rtsp视频流\n
    Args:\n
        ip_address: str ip地址，用于获取网段
        user: str 用户名
        pwd: str 密码
        port: int 端口
    Returns:\n
        rtsp_url_list list rtsp地址列表
    Demo:\n
        >>> scan_rtsp(get_ip('192.168.1.')[0], 'admin', 'Hik@sxxs4500')
    """
    rtsp_url_list = []
    if not check_ip(ip_address):
        return rtsp_url_list
    ip_address_list = scan_ip(ip_address)
    q = Queue()
    for ip in ip_address_list:
        if user and pwd:
            rtsp_url = 'rtsp://' + user + ':' + pwd + '@' + ip
        else:
            rtsp_url = 'rtsp://' + ip
        # 如果端口是554就可以省略不写了
        if port and port != RTSP_PORT:
            rtsp_url += ':' + str(port)
        q.put(rtsp_url)
    _shot_fun(q, rtsp_url_list)
    q.join()
    # 排序
    rtsp_url_list.sort(key=lambda x: int(extract_ip(x['rtsp_url']).split('.')[-1]))
    return rtsp_url_list


@parallel_execute(32)
def _shot_fun(in_queue, out_list):
    while not in_queue.empty():
        rtsp_url = in_queue.get()
        if not check_rtsp(rtsp_url):
            in_queue.task_done()
        image_path = save_screenshot(rtsp_url)
        if image_path:
            out_list.append({'rtsp_url': rtsp_url, 'image_path': image_path})
        in_queue.task_done()

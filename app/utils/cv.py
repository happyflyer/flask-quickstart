# -*- coding: utf-8 -*-

import os
from datetime import datetime

import cv2

from .dt import TIMESTAMP_FORMATTER


def save_screenshot(filename, image_dir='tmp', image_prefix='screenshot', image_suffix=TIMESTAMP_FORMATTER):
    """保存视频文件、图片文件、视频流的截图

    Args:
        filename (str): 视频文件名、图片文件名、视频流 url
        image_dir (str, optional): 截图文件保存文件夹. Defaults to 'tmp'.
        image_prefix (str, optional): 截图文件名前缀. Defaults to 'screenshot'.
        image_suffix (str, optional): 截图文件名后缀，用于时间戳格式化. Defaults to '%Y%m%d_%H%M%S_%f'.

    Returns:
        str: 截图文件路径，当 filename 不可用时返回None

    Examples:
        >>> save_screenshot('rtsp://admin:123456@192.168.1.3')
    """
    # FIXME: 如果视频流地址不可用，此语句会阻塞
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        image_name = '_'.join([image_prefix, datetime.utcnow().strftime(image_suffix)])
        image_name = '.'.join([image_name, 'jpg'])
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_path = os.path.join(image_dir, image_name)
        ret, frame = cap.read()
        cv2.imwrite(image_path, frame)
        cap.release()
        return image_path
    cap.release()
    return None

# -*- coding: utf-8 -*-

import os
from datetime import datetime

import cv2


__all__ = [
    'save_screenshot'
]


def save_screenshot(filename, image_dir='tmp', image_prefix='screenshot', image_suffix='%Y%m%d_%H%M%S_%f'):
    """保存视频文件、图片文件、视频流的截图\n
    Args:\n
        filename str 视频文件名、图片文件名、视频流url
        image_dir str 截图文件保存文件夹
        image_prefix str 截图文件名前缀
        image_suffix str 截图文件名后缀，用于时间戳格式化
    Returns:\n
        image_path str 截图文件路径，当流文件不可用时，返回None
    Demo:\n
        >>> save_screenshot('rtsp://admin:Hik@sxxs4500@192.168.1.3')
    """
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

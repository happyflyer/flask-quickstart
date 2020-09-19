# -*- coding: utf-8 -*-

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """api请求的错误处理函数

    Args:
        status_code (int): HTTP状态码
        message (str, optional): 提示消息. Defaults to None.

    Returns:
        dict: 非法请求响应格式，示例：

        {
            'error': 'short error description',
            'message': 'error message (optional)'
        }
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """请求不合法

    Args:
        message (str): 提示消息

    Returns:
        dict: 返回400状态码
    """
    return error_response(400, message)


def forbidden(message):
    """禁止访问

    Args:
        message (str): 提示消息

    Returns:
        dict: 返回403状态码
    """
    return error_response(403, message)


def not_found(message):
    """页面未找到

    Args:
        message (str): 提示消息

    Returns:
        dict: 返回404状态码
    """
    return error_response(404, message)

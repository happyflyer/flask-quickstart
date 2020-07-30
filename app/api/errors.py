# -*- coding: utf-8 -*-

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """非法请求的响应\n
    Returns:\n
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
    """请求不合法\n
    Args:\n
        message str
    """
    return error_response(400, message)

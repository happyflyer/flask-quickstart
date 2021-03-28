__all__ = [
    'error_response',
    'bad_request',
    'unauthorized',
    'forbidden',
    'not_found'
]

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """api请求的错误处理函数
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """请求参数错误
    """
    return error_response(400, message)


def unauthorized(message):
    """未认证
    """
    return error_response(401, message)


def forbidden(message):
    """禁止访问
    """
    return error_response(403, message)


def not_found(message):
    """资源未找到
    """
    return error_response(404, message)

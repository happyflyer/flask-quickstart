# -*- coding: utf-8 -*-

from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from ..models import User
from .errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """http基本认证的处理函数

    Args:
        username (str): 用户名
        password (str): 密码

    Returns:
        bool: 密码校验结果
    """
    user = User.query.filter(User.username == username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    """http基本认证未通过的处理函数

    Returns:
        dict: 返回401状态码
    """
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    """token认证的处理函数

    Args:
        token (str): token

    Returns:
        User: token 认证结果，找不到用户时返回None
    """
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    """token认证未通过的处理函数

    Returns:
        dict: 返回401状态码
    """
    return error_response(401)

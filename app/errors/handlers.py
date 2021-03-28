from flask import render_template, request

from .. import db
from ..api import error_response as api_error_response
from . import bp


def wants_json_response():
    """是否使用api的错误处理函数
    """
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(400)
def bad_request(error):
    """请求参数错误
    """
    if wants_json_response():
        return api_error_response(400)
    return render_template('errors/400.jinja2'), 400


@bp.app_errorhandler(403)
def forbidden(error):
    """禁止访问
    """
    if wants_json_response():
        return api_error_response(403)
    return render_template('errors/403.jinja2'), 403


@bp.app_errorhandler(404)
def not_found(error):
    """资源未找到
    """
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.jinja2'), 404


@bp.app_errorhandler(405)
def method_not_allowed(error):
    """方法不允许
    """
    if wants_json_response():
        return api_error_response(405)
    return render_template('errors/405.jinja2'), 405


@bp.app_errorhandler(500)
def internal_server_error(error):
    """服务器内部错误
    """
    # 发生服务器内部错误时，需要回滚数据库事务
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.jinja2'), 500

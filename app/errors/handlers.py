# -*- coding: utf-8 -*-

from flask import render_template, request

from .. import db
from . import bp
from ..api import error_response as api_error_response


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(403)
def forbidden_error(error):
    if wants_json_response():
        return api_error_response(403)
    return render_template('errors/403.jinja2'), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.jinja2'), 404


@bp.app_errorhandler(405)
def method_not_allowed(error):
    if wants_json_response():
        return api_error_response(405)
    return render_template('errors/405.jinja2'), 405


@bp.app_errorhandler(500)
def internal_error(error):
    # 发生服务器内部错误时，回滚数据库事务
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.jinja2'), 500

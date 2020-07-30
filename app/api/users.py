# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask_babel import lazy_gettext as _l

from .. import db, write_required, read_required, WRITE_PERMISSION, MODULES, PERMISSIONS
from ..models import User
from . import bp, RECORDS_PER_PAGE, RECORDS_MAX_PER_PAGE, token_auth, bad_request


@bp.route('/user', methods=['GET'])
@token_auth.login_required
@write_required(module='main')
def get_users():
    """获取所有用户
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    > 访问用户对 main 模块有 W 权限。\n
    #### return
    ```json
    {
        "_links": {
            "next": null,
            "prev": null,
            "self": "/api/user?page=1&per_page=25"
        },
        "_meta": {
            "page": 1,
            "per_page": 25,
            "total_items": 4,
            "total_pages": 1
        },
        "items": [
            {
            "last_visit": "2020-07-30 04:04:26",
            "permission": "22222222222222222222222222222222",
            "user_id": 1,
            "username": "admin"
            },
            {
            "last_visit": "2020-07-30 03:48:56",
            "permission": "10000000000000000000000000000000",
            "user_id": 2,
            "username": "test"
            }
        ]
    }
    ```
    @@@
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', RECORDS_PER_PAGE, type=int)
    per_page = min(per_page, RECORDS_MAX_PER_PAGE)
    payload = User.to_collection_dict(User.query.order_by(User.id.asc()), page, per_page, 'api.get_users')
    return jsonify(payload)


@bp.route('/user/<string:username>', methods=['GET'])
@token_auth.login_required
@read_required(module='main')
def get_user_by_username(username):
    """通过用户名获取用户
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    > 访问用户对 main 模块有 R 权限。\n
    #### return
    ```json
    {
        "last_visit": "2020-07-30 04:04:26",
        "permission": "22222222222222222222222222222222",
        "user_id": 1,
        "username": "admin"
    }
    ```
    @@@
    """
    user = User.query.filter(User.username == username).first_or_404()
    return jsonify(user.to_dict())


@bp.route('/user/add', methods=['POST'])
@token_auth.login_required
@write_required(module='main')
def add_user():
    """新增用户
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    > 访问用户对 main 模块有 W 权限。\n
    > 新增的用户对所有模块的权限都默认为 N 权限。\n
    | 字段     | 是否必须 | 类型 | 说明   |
    | -------- | -------- | ---- | ------ |
    | username | true     | str  | 用户名 |
    | password | true     | str  | 密码   |
    #### return
    ```json
    {
        "last_visit": "2020-07-30 06:26:37",
        "permission": "00000000000000000000000000000000",
        "user_id": 3,
        "username": "my_user"
    }
    ```
    @@@
    """
    form_data = request.form.to_dict()
    user = User()
    user = user.from_dict(form_data, new_user=True)
    if not user:
        return bad_request(_l('missing username!'))
    if User.query.filter(User.username == user.username).count() > 0:
        return bad_request(_l('%(username)s already exists!', username=user.username))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/user/<string:username>/grant', methods=['POST'])
@token_auth.login_required
@write_required(module='main')
def grant_user(username):
    """给用户授权
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    > 访问用户对 main 模块有 W 权限。\n
    > 新增的用户对所有模块的权限都默认为 N 权限。\n
    | 字段       | 是否必须 | 类型 | 说明     |
    | ---------- | -------- | ---- | -------- |
    | module     | true     | str  | 模块名   |
    | permission | true     | int  | 权限级别 |
    #### return
    ```json
    {
        "last_visit": "2020-07-30 06:26:37",
        "permission": "10000000000000000000000000000000",
        "user_id": 3,
        "username": "my_user"
    }
    ```
    @@@
    """
    form_data = request.form.to_dict()
    if 'module' not in form_data or 'permission' not in form_data:
        return bad_request(_l('missing module or permission!'))
    module = form_data.get('module')
    permission = int(form_data.get('permission'))
    if module not in MODULES or permission not in PERMISSIONS:
        return bad_request(_l('invalid module or permission!'))
    user = User.query.filter(User.username == username).first_or_404()
    if not user:
        return bad_request(_l('missing username!'))
    # admin必须具有main模块的W权限
    if user.username == 'admin' and module == 'main' and permission < WRITE_PERMISSION:
        return bad_request(_l('%(username)s must have %(permission)s to %(module)s!',
            username='admin', permission=PERMISSIONS[WRITE_PERMISSION], module='main'))  # NOQA
    user.set_permission(module, permission)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/module', methods=['GET'])
@token_auth.login_required
@read_required(module='main')
def get_modules():
    """获取所有模块
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    > 访问用户对 main 模块有 R 权限。\n
    #### return
    ```json
    {
        "api": 1,
        "main": 0
    }
    ```
    @@@
    """
    return jsonify(MODULES)


@bp.route('/permission', methods=['GET'])
@token_auth.login_required
@read_required(module='main')
def get_permissions():
    """获取所有权限
    @@@
    #### args
    > 在 request 请求头中携带 `Authorization` 字段。\n
    > 访问用户对 main 模块有 R 权限。\n
    #### return
    ```json
    {
        "0": "N",
        "1": "R",
        "2": "W"
    }
    ```
    @@@
    """
    return jsonify(PERMISSIONS)

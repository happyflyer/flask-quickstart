# -*- coding: utf-8 -*-

from flask import request, jsonify, g
from flask_babel import lazy_gettext as _l

from ... import db, write_required, read_required, RECORDS_PER_PAGE, RECORDS_MAX_PER_PAGE, WRITE_PERMISSION, MODULES, PERMISSIONS
from ...api import token_auth, bad_request, forbidden
from ...models import User
from . import bp


@bp.route('/user', methods=['GET'])
@token_auth.login_required
@write_required()
def get_users():
    """获取所有用户

    @@@
    ## 请求头

    - 携带 `Authorization` 字段。

    ## 权限

    - 访问用户对 main_api 模块有 W 权限。

    ## 查询字段

    | 字段     | 是否必须 | 类型 | 说明     |
    | -------- | -------- | ---- | -------- |
    | username |          | str  | 模糊查询 |
    | page     |          | int  | 默认：1  |
    | per_page |          | int  | 默认：25 |

    ## 响应示例

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
            }
        ]
    }
    ```

    @@@
    """
    username = request.args.get('username', None, type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', RECORDS_PER_PAGE, type=int)
    per_page = min(per_page, RECORDS_MAX_PER_PAGE)
    custom_query = User.query
    if username:
        custom_query = custom_query.filter(User.username.like('%' + username + '%'))
    custom_query = custom_query.order_by(User.id.asc())
    payload = User.to_collection_dict(custom_query, page, per_page, 'main_api.get_users',
        username=username)  # NOQA
    return jsonify(payload)


@bp.route('/user/<string:username>', methods=['GET'])
@token_auth.login_required
@read_required()
def get_user(username):
    """获取单个用户

    @@@
    ## 请求头

    - 携带 `Authorization` 字段。

    ## 权限

    - 访问用户对 main_api 模块有 R 权限。
    - 访问用户获取其他用户信息时，需要对 main_api 模块有 W 权限。

    ## 响应示例

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
    # 获取其他用户信息时，需要main模块的W权限
    if g.current_user.username != username:
        if not g.current_user.check_permission('main_api', WRITE_PERMISSION):
            return forbidden(_l('insufficient permission!'))
    user = User.query.filter(User.username == username).first_or_404()
    return jsonify(user.to_dict())


@bp.route('/user/add', methods=['POST'])
@token_auth.login_required
@write_required()
def add_user():
    """新增用户

    @@@
    ## 请求头

    - 携带 `Authorization` 字段。\n

    ## 权限

    - 访问用户对 main_api 模块有 W 权限。\n
    - 新增的用户对所有模块的权限都默认为 N 权限。\n

    ## 表单字段

    | 字段     | 是否必须 | 类型 | 说明   |
    | -------- | -------- | ---- | ------ |
    | username | 是       | str  | 用户名 |
    | password | 是       | str  | 密码   |

    ## 响应示例

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
    user = User.from_dict(form_data)
    if user is None:
        return bad_request(_l('missing username!'))
    # 用户名重复检查
    if User.query.filter(User.username == user.username).count() > 0:
        return bad_request(_l('%(username)s already exists!', username=user.username))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/user/grant/<string:username>', methods=['POST'])
@token_auth.login_required
@write_required()
def grant_user(username):
    """用户授权

    @@@
    ## 请求头

    - 携带 `Authorization` 字段。\n

    ## 权限

    - 访问用户对 main_api 模块有 W 权限。\n

    ## 表单字段

    | 字段       | 是否必须 | 类型 | 说明     |
    | ---------- | -------- | ---- | -------- |
    | module     | 是       | str  | 模块名   |
    | permission | 是       | int  | 权限级别 |

    ## 响应示例

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
    # 模块和权限检查
    if 'module' not in form_data or 'permission' not in form_data:
        return bad_request(_l('missing module or permission!'))
    module_name = form_data.get('module')
    permission = int(form_data.get('permission'))
    if module_name not in MODULES or permission not in PERMISSIONS:
        return bad_request(_l('invalid module or permission!'))
    # 用户存在检查
    user = User.query.filter(User.username == username).first_or_404()
    if not user:
        return bad_request(_l('missing username!'))
    # admin必须具有main_api模块的W权限
    if username == 'admin' and (module_name == 'main' or module_name == 'main_api') and permission < WRITE_PERMISSION:
        return bad_request(_l('%(username)s must have %(permission)s to %(module)s!',
            username=username, permission=PERMISSIONS[WRITE_PERMISSION], module=module_name))  # NOQA
    user.set_permission(module_name, permission)
    db.session.commit()
    return jsonify(user.to_dict())

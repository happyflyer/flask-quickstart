from flask import request, jsonify, g
from flask_babel import lazy_gettext as _l
from ... import db, csrf
from ...api import token_auth, bad_request, forbidden
from ...models import User
from ...modules import *
from ...page import *
from ...permission import *
from .. import bp


@bp.route('/user', methods=['GET'])
@token_auth.login_required
@write_required()
def list_users_api():
    """获取所有用户

    @@@
    ### 权限
    - 访问用户需登录，请求头携带 `Authorization` 字段。
    - 访问用户对 main 模块有 WRITE 权限。

    ### 查询字段
    | 字段     | 是否必须 | 类型 | 说明         |
    | -------- | -------- | ---- | ------------ |
    | username |          | str  | 支持模糊查询 |
    | page     |          | int  | 默认：1      |
    | per_page |          | int  | 默认：25     |

    @@@
    """
    username = request.args.get('username', None, type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', RECORDS_PER_PAGE, type=int)
    per_page = min(per_page, MAX_RECORDS_PER_PAGE)
    custom_query = User.query
    if username:
        custom_query = custom_query.filter(User.username.like('%' + username + '%'))
    custom_query = custom_query.order_by(User.id.asc())
    payload = User.to_collection_dict(
        custom_query,
        page,
        per_page,
        'main.list_users_api',
        username=username
    )
    return jsonify(payload)


@bp.route('/user/<string:username>', methods=['GET'])
@token_auth.login_required
@read_required()
def get_user_api(username):
    """获取单个用户

    @@@
    ### 权限
    - 访问用户需登录，请求头携带 `Authorization` 字段。
    - 访问用户对 main 模块有 READ 权限。
    - 访问用户获取其他用户信息时，需要对 main 模块有 WRITE 权限。

    @@@
    """
    # 获取其他用户信息时，需要main模块的WRITE权限
    if g.current_user.username != username:
        if not g.current_user.check_permission('main', WRITE_PERMISSION):
            return forbidden(_l('insufficient permission!'))
    user = User.query.filter(User.username == username).first_or_404()
    return jsonify(user.to_dict())


@bp.route('/user/add', methods=['POST'])
@csrf.exempt
@token_auth.login_required
@write_required()
def add_user_api():
    """新增用户

    @@@
    ### 权限
    - 访问用户需登录，请求头携带 `Authorization` 字段。
    - 访问用户对 main 模块有 WRITE 权限。

    ### 表单字段
    | 字段     | 是否必须 | 类型 | 说明   |
    | -------- | -------- | ---- | ------ |
    | username | 是       | str  | 用户名 |
    | password | 是       | str  | 密码   |

    @@@
    """
    form_data = request.form.to_dict()
    user = User.from_dict(form_data)
    if user is None:
        return bad_request(_l('missing username!'))
    # 用户名重复检查
    if User.query.filter(User.username == user.username).count() > 0:
        return bad_request(_l(
            '%(username)s already exists!',
            username=user.username
        ))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/user/grant/<string:username>', methods=['POST'])
@csrf.exempt
@token_auth.login_required
@write_required()
def grant_user_api(username):
    """授权单个用户

    @@@
    ### 权限
    - 访问用户需登录，请求头携带 `Authorization` 字段。
    - 访问用户对 main 模块有 WRITE 权限。

    ### 表单字段
    | 字段       | 是否必须 | 类型 | 说明     |
    | ---------- | -------- | ---- | -------- |
    | module     | 是       | str  | 模块名   |
    | permission | 是       | int  | 权限级别 |

    @@@
    """
    form_data = request.form.to_dict()
    # 检查 module
    if 'module' not in form_data:
        return bad_request(_l('missing module'))
    module = form_data.get('module')
    if module not in MODULES:
        return bad_request(_l('invalid module!'))
    # 检查 permission
    if 'permission' not in form_data:
        return bad_request(_l('missing permission!'))
    permission = int(form_data.get('permission'))
    if permission not in PERMISSIONS:
        return bad_request(_l('invalid permission!'))
    user = User.query.filter(User.username == username).first_or_404()
    # admin 必须具有 main 模块的 WRITE 权限
    if username == 'admin' and module == 'main' and permission < WRITE_PERMISSION:
        return bad_request(_l('admin must have WRITE permission on main module!'))
    # 设置其他用户的权限
    user.set_permission(module, permission)
    db.session.commit()
    return jsonify(user.to_dict())

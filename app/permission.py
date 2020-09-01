# -*- coding: utf-8 -*-

from functools import partial, wraps

from flask import request, abort, g


__all__ = [
    'NO_PERMISSION',
    'READ_PERMISSION',
    'WRITE_PERMISSION',
    'PERMISSIONS',
    'read_required',
    'write_required'
]

# 权限控制要求用户登录，匿名用户没有权限控制
NO_PERMISSION = 0
READ_PERMISSION = 1
WRITE_PERMISSION = 2
PERMISSIONS = {
    NO_PERMISSION: 'N',
    READ_PERMISSION: 'R',
    WRITE_PERMISSION: 'W'
}


def _custom_required(permission, *args, **kw_args):
    """访问用户对指定模块有permission权限

    Args:
        permission (int): 权限级别

    Returns:
        None: 权限验证通过时执行函数，权限验证不通过时返回403状态码
    """
    def _permission_required(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            module = request.blueprint
            if kw_args.get('module'):
                module = kw_args.get('module') or 0
            if g.current_user and g.current_user.is_anonymous or \
                    not g.current_user.check_permission(module, permission):
                abort(403)
            return func(*args, **kwargs)
        return decorated_view
    return _permission_required


read_required = partial(_custom_required, permission=READ_PERMISSION)
write_required = partial(_custom_required, permission=WRITE_PERMISSION)

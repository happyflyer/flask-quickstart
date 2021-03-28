"""访问权限控制
"""

__all__ = [
    'NO_PERMISSION',
    'READ_PERMISSION',
    'WRITE_PERMISSION',
    'PERMISSIONS',
    'read_required',
    'write_required'
]

from functools import partial, wraps
from flask import request, abort, g

NO_PERMISSION = 0
READ_PERMISSION = 1
WRITE_PERMISSION = 2
PERMISSIONS = {
    NO_PERMISSION: 'NO',
    READ_PERMISSION: 'READ',
    WRITE_PERMISSION: 'WRITE'
}


def _custom_required(permission, *args, **kw_args):
    """访问用户对指定模块有permission权限
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

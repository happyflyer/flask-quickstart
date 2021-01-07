"""数据库初始化
"""

from . import db
from .utils import read_json


def init_users():
    payload = read_json('data/models.json')
    from .models import User, DEFAULT_NEW_USER_PERMISSIONS
    with db.get_app().app_context():
        items_ready_add = []
        for item in payload.get('users'):
            if User.query.filter(User.username == item.get('username')).count() == 0:
                user = User.from_dict(item)
                if user:
                    user.set_all_permissions(item.get('permission') or DEFAULT_NEW_USER_PERMISSIONS)
                    items_ready_add.append(user)
            else:
                res = User.query.filter(User.username == item.get('username')).first()
                res = User.from_dict(item, res)
                res.set_all_permissions(item.get('permission') or DEFAULT_NEW_USER_PERMISSIONS)
                db.session.commit()
        if items_ready_add:
            db.session.add_all(items_ready_add)
            db.session.commit()

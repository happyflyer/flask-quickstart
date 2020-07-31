# -*- coding: utf-8 -*-

from . import db
from .models import User
from .utils import read_json


def init_users():
    payload = read_json('data/models.json')
    with db.get_app().app_context():
        items_ready_add = []
        for item in payload['users']:
            if User.query.filter(User.username == item['username']).count() == 0:
                user = User.from_dict(item, new_user=True)
                user.set_all_permissions(item['permission'])
                items_ready_add.append(user)
        db.session.add_all(items_ready_add)
        db.session.commit()

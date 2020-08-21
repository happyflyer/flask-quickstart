# -*- coding: utf-8 -*-

import base64
import json
import os
from datetime import datetime, timedelta

from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login, MODULES, MODULES_NUMBER, EXCLUDED_ENDPOINTS,\
    NO_PERMISSION, READ_PERMISSION, WRITE_PERMISSION, PERMISSIONS, DEFAULT_PERMISSION
from .utils import ENCODING, DATETIME_FORMATTER


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """获取分页数据\n
        Args:\n
            query BaseQuery
            page int 请求页码
            per_page int 每页记录数量
            endpoint endpoint
        Returns:\n
            {
                "items": [
                    { ... item resource ... },
                    { ... item resource ... },
                    ...
                ],
                "_meta": {
                    "page": 1,
                    "per_page": 10,
                    "total_pages": 20,
                    "total_items": 195
                },
                "_links": {
                    "self": "http://localhost:5000/api/users?page=1",
                    "next": "http://localhost:5000/api/users?page=2",
                    "prev": null
                }
            }
        """
        resources = query.paginate(page, per_page, False)
        payload = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return payload


class User(PaginatedAPIMixin, UserMixin, db.Model):
    __tablename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True)
    # 用于登录的用户名，不能重复
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(MODULES_NUMBER), server_default=DEFAULT_PERMISSION)
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    visit_logs = db.relationship('VisitLog', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """设置密码\n
        Args:\n
            password str
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码\n
        Args:\n
            password str
        Returns:\n
            True or False
        """
        return check_password_hash(self.password_hash, password)

    def set_all_permissions(self, all_permissions):
        """设置所有模块权限\n
        Args:\n
            all_permissions str 长度为MODULES_NUMBER的权限控制字符串
        """
        if len(all_permissions) != MODULES_NUMBER:
            raise RuntimeError('Invalid all_permissions!')
        self.permission = all_permissions

    def set_permission(self, module_name, permission):
        """设置单个模块权限\n
        Args:\n
            module_name str 模块名
            permission int 权限值，可以为0，1，2，分别代表无权限，读权限，写权限
        """
        module_bit = MODULES.get(module_name)
        if module_bit is None:
            raise RuntimeError('Invalid module!')
        if permission not in PERMISSIONS:
            raise RuntimeError('Invalid permission!')
        self.permission = ''.join([self.permission[:module_bit], str(permission), self.permission[module_bit+1:]])

    def check_permission(self, module_name, permission):
        """验证权限\n
        Args:\n
            module_name str 模块名
            permission int 权限值，可以为0，1，2，分别代表无权限，读权限，写权限
        Returns:\n
            True or False
        """
        module_bit = MODULES.get(module_name)
        if module_bit is None:
            return False
        if permission not in PERMISSIONS:
            return False
        user_premission = int(self.permission[module_bit])
        return user_premission >= permission

    def check_read_permission(self, module_name):
        """验证读权限\n
        Args:\n
            module_name str 模块名
        Returns:\n
            True or False
        """
        return self.check_permission(module_name, READ_PERMISSION)

    def check_write_permission(self, module_name):
        """验证写权限\n
        Args:\n
            module_name str 模块名
        Returns:\n
            True or False
        """
        return self.check_permission(module_name, WRITE_PERMISSION)

    def to_dict(self):
        """序列化为json\n
        Returns:\n
            {
                'user_id': 2,
                'username': 'test',
                'last_visit': NULL,
                'permission': 11000000000000000000000000000000
            }
        """
        payload = {
            'user_id': self.id,
            'username': self.username,
            'last_visit': self.last_visit.strftime(DATETIME_FORMATTER) if self.last_visit else None,
            'permission': self.permission
        }
        return payload

    @staticmethod
    def from_dict(payload, new_user=False):
        """从json解析\n
        Args:\n
            payload dict 至少包含username
            new_user bool 是否为新用户，新用户将从payload解析password，并设置password
        Returns:\n
            user User 根据payload解析得到的user对象，如果payload中缺少必要的字段，将返回None
        """
        required_fields = ['username']
        for field in required_fields:
            if field not in payload:
                return None
        user = User()
        user.username = payload.get('username')
        if new_user and 'password' in payload:
            user.set_password(payload.get('password'))
        return user

    def get_token(self, expires_in=24):
        """获得token\n
        Args:\n
            expires_in int 失效时间，单位为小时
        Returns:\n
            token str
        """
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        # 32位长度的字符串token
        self.token = base64.b64encode(os.urandom(24)).decode(ENCODING)
        self.token_expiration = now + timedelta(hours=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """失效token\n
        """
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        """验证token\n
        Args:\n
            token str
        Returns:\n
            user User
        """
        user = User.query.filter(User.token == token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def add_visit_log(self, request, response):
        """新增访问记录\n
        Args:\n
            request Request
            response Response
        Returns:\n
            visit_log VisitLog
        """
        if request.blueprint in MODULES and request.endpoint not in EXCLUDED_ENDPOINTS:
            visit_log = VisitLog(
                url=request.url[:200],
                method=request.method[:10],
                user=self,
                timestamp=datetime.utcnow(),
                scheme=request.scheme[:10],
                host=request.host[:20],
                path=request.path[:50],
                query_string=bytes.decode(request.query_string, ENCODING)[:100],
                json=json.dumps(request.form.to_dict())[:200],
                blueprint=request.blueprint[:20],
                endpoint=request.endpoint[:50],
                remote_addr=request.remote_addr[:20],
                user_agent=str(request.user_agent)[:200],
                status_code=str(response.status_code)[:10]
            )
            db.session.add(visit_log)
            return visit_log
        else:
            return None


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class VisitLog(db.Model):
    __tablename__ = 'sys_visit_log'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    method = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # url
    scheme = db.Column(db.String(10))
    host = db.Column(db.String(20))
    path = db.Column(db.String(50))
    query_string = db.Column(db.String(100))
    json = db.Column(db.String(200))
    # module
    blueprint = db.Column(db.String(20))
    endpoint = db.Column(db.String(50))
    # browser
    remote_addr = db.Column(db.String(20))
    user_agent = db.Column(db.String(200))
    # response
    status_code = db.Column(db.String(10))

    def __repr__(self):
        return '<VisitLog {}>'.format(self.url)

    def to_dict(self):
        """序列化为json\n
        Returns:\n
            {
                'url': 'http://localhost:5000/',
                'method': 'GET',
                'timestamp': NULL,
                'endpoint': 'main.index',
                'status_code': 200
            }
        """
        payload = {
            'url': self.url,
            'method': self.method,
            'timestamp': self.timestamp.strftime(DATETIME_FORMATTER) if self.timestamp else None,
            'endpoint': self.endpoint,
            'status_code': self.status_code
        }
        return payload

import base64
import json
import os
from datetime import datetime, timedelta
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login
from .modules import *
from .permission import *
from .utils import datetime_format

_encoding = 'utf-8'
DEFAULT_NO_PERMISSIONS = str(NO_PERMISSION)*MAX_MODULES_NUMBER
DEFAULT_NEW_USER_PERMISSIONS = str(READ_PERMISSION)*2 + str(NO_PERMISSION)*(MAX_MODULES_NUMBER-2)


class PaginatedAPIMixin(object):
    """分页数据格式

    ```
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
    ```
    """
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """获得分页数据

        Args:
            query (BaseQuery): orm查询
            page (int): 页码
            per_page (int): 每页条数
            endpoint (function): 端点函数

        Returns:
            dict: 分页数据
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
                'self': url_for(
                    endpoint,
                    page=page,
                    per_page=per_page,
                    **kwargs
                ),
                'next': url_for(
                    endpoint,
                    page=page + 1,
                    per_page=per_page,
                    **kwargs
                ) if resources.has_next else None,
                'prev': url_for(
                    endpoint,
                    page=page - 1,
                    per_page=per_page,
                    **kwargs
                ) if resources.has_prev else None
            }
        }
        return payload


class User(PaginatedAPIMixin, UserMixin, db.Model):
    """系统用户
    """
    __tablename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True)
    # 用于登录的用户名，不能重复
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(MAX_MODULES_NUMBER))
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    visit_logs = db.relationship('VisitLog', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """设置密码
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """检查密码
        """
        return check_password_hash(self.password_hash, password)

    def set_all_permissions(self, all_permissions=DEFAULT_NEW_USER_PERMISSIONS):
        """设置所有模块权限
        """
        if len(all_permissions) != MAX_MODULES_NUMBER:
            raise RuntimeError('invalid all_permissions!')
        self.permission = all_permissions

    def set_permission(self, module_name, permission=NO_PERMISSION):
        """设置单个模块权限
        """
        module_bit = MODULES.get(module_name)
        if module_bit is None:
            raise RuntimeError('invalid module_name!')
        if permission not in PERMISSIONS:
            raise RuntimeError('invalid permission!')
        self.permission = ''.join([
            self.permission[:module_bit],
            str(permission),
            self.permission[module_bit+1:]
        ])

    def check_permission(self, module_name, permission):
        """验证权限
        """
        module_bit = MODULES.get(module_name)
        if module_bit is None:
            return False
        if permission not in PERMISSIONS:
            return False
        user_premission = int(self.permission[module_bit])
        return user_premission >= permission

    def check_read_permission(self, module_name):
        """验证读权限
        """
        return self.check_permission(module_name, READ_PERMISSION)

    def check_write_permission(self, module_name):
        """验证写权限
        """
        return self.check_permission(module_name, WRITE_PERMISSION)

    def to_dict(self):
        """序列化object为dict
        """
        payload = {
            'user_id': self.id,
            'username': self.username,
            'last_visit': datetime_format(self.last_visit),
        }
        return payload

    @staticmethod
    def from_dict(payload, obj=None):
        """从dict反序列化object
        """
        required_fields = ['username']
        if obj is None:
            for field in required_fields:
                if field not in payload:
                    return None
            obj = User()
            obj.username = payload.get('username', '')[:20]
            obj.set_all_permissions()
        if 'password' in payload:
            obj.set_password(payload.get('password'))
        return obj

    def get_token(self, expires_in=24*7):
        """获得token
        """
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        # 32位长度的字符串token
        self.token = base64.b64encode(os.urandom(24)).decode(_encoding)
        self.token_expiration = now + timedelta(hours=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """失效token
        """
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        """检查token
        """
        user = User.query.filter(User.token == token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def add_visit_log(self, request, response):
        """新增访问记录
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
                query_string=bytes.decode(request.query_string, _encoding)[:100],
                json=json.dumps(request.form.to_dict())[:200],
                blueprint=request.blueprint[:20],
                endpoint=request.endpoint[:50],
                remote_addr=request.headers.get('X-Forwarded-For', '')[:20],
                user_agent=str(request.user_agent)[:200],
                status_code=str(response.status_code)[:10]
            )
            db.session.add(visit_log)
            return visit_log
        else:
            return None


@login.user_loader
def load_user(id):
    """登录处理函数
    """
    return User.query.get(int(id))


class VisitLog(db.Model):
    """访问记录
    """
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
        """序列化object为dict
        """
        payload = {
            'url': self.url,
            'method': self.method,
            'timestamp': datetime_format(self.timestamp),
            'endpoint': self.endpoint,
            'status_code': self.status_code
        }
        return payload

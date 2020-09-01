# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

from flask import Flask, request, g, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_docs import ApiDoc

from config import Config
from .permission import *


# https://semver.org/lang/zh-CN/
# 版本格式：主版本号.次版本号.修订号，版本号递增规则如下：
# 主版本号：当你做了不兼容的 API 修改，
# 次版本号：当你做了向下兼容的功能性新增，
# 修订号：当你做了向下兼容的问题修正。
__version__ = '0.2.12'

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
babel = Babel()
csrf = CSRFProtect()
doc = ApiDoc()

# 每页记录数
RECORDS_PER_PAGE = 25
# 每页最大记录数
RECORDS_MAX_PER_PAGE = 50
# 用于访问统计、权限控制的模块
MODULES = {
    'main': 0,
    'api': 1
}
# 用于访问统计、权限控制的模块数量
MODULES_NUMBER = 32
# 新用户默认权限
DEFAULT_PERMISSION = str(READ_PERMISSION) * 2 + str(NO_PERMISSION) * (MODULES_NUMBER - 2)
# 不用于访问统计的endpoint
EXCLUDED_ENDPOINTS = [
    'main.favicon'
]


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    CORS(app, supports_credentials=True)
    doc.init_app(app, title=_l('Flask Quickstart'), version=__version__)

    from .errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/')
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    from .main.api import bp as main_api_bp
    app.register_blueprint(main_api_bp, url_prefix='/main/api')
    csrf.exempt(main_api_bp)
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    csrf.exempt(api_bp)

    app.jinja_env.globals['str'] = str
    app.jinja_env.globals['int'] = int
    app.jinja_env.globals['max'] = max
    app.jinja_env.globals['min'] = min
    from .momentjs import MomentJs
    app.jinja_env.globals['moment'] = MomentJs

    @app.before_first_request
    def before_first_request():
        """应用程序启动后，在处理第一个请求前执行。通常做数据初始化等"""
        from . import database
        database.init_users()

    @app.before_request
    def before_request():
        """在每次处理请求前执行。通常做用户权限校验、本地化处理等"""
        if current_user.is_authenticated:
            current_user.last_visit = datetime.utcnow()
            db.session.commit()
            g.current_user = current_user
        g.locale = get_locale()

    @app.after_request
    def after_request(response):
        """每次请求之后调用。前提是没有未处理的异常抛出。通常做用户操作日志等"""
        if hasattr(g, 'current_user') and g.current_user and g.current_user.is_authenticated:
            g.current_user.add_visit_log(request, response)
            db.session.commit()
        return response

    @app.teardown_request
    def teardown_request(exc):
        """每次请求之后调用，不管处理请求过程中是否出现异常。通常是释放数据库连接等"""
        pass

    if not app.debug:
        # 文件日志
        if not os.path.exists('log'):
            os.makedirs('log')
        file_handler = TimedRotatingFileHandler(os.path.join(
            'log', 'app.log'), when='D', interval=1, backupCount=10,
            encoding='utf-8', delay=False, utc=True)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
        # 邮件日志
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_ADMINS'][0],
                toaddrs=app.config['MAIL_ADMINS'],
                subject='Your App Failure',
                credentials=auth,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('app has been created.')

    return app


@babel.localeselector
def get_locale():
    """获得本地区域设置

    Returns:
        str: 语言_地区
    """
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from . import models  # NOQA
from . import beans  # NOQA

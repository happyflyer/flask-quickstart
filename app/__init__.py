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
from flask_apscheduler import APScheduler
from config import Config

# https://semver.org/lang/zh-CN/
__version__ = '0.4.5'
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
babel = Babel()
csrf = CSRFProtect()
cors = CORS()
doc = ApiDoc()
scheduler = APScheduler()


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
    cors.init_app(app, supports_credentials=True)
    doc.init_app(app, title=app.config.get('APP_NAME'), version=__version__)
    if app.debug:
        scheduler.init_app(app)
        scheduler.start()
    elif app.testing:
        pass
    else:
        from .apscheduler import init_apscheduler
        init_apscheduler(app, scheduler)
        from . import jobs
        jobs.do_jobs()
    # errors
    from .errors import bp as errors_bp
    app.register_blueprint(errors_bp, url_prefix='/')
    # auth
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # main
    from .main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    # api
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
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
        import shutil
        shutil.rmtree('tmp', ignore_errors=True)

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
        file_handler = TimedRotatingFileHandler(
            os.path.join('log', 'app.log'), when='D', interval=1,
            backupCount=10, encoding='utf-8', delay=False, utc=True)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
        # 邮件日志
        if app.config.get('MAIL_SERVER'):
            auth = None
            if app.config.get('MAIL_USERNAME') or app.config.get('MAIL_PASSWORD'):
                auth = (app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD'))
            secure = None
            if app.config.get('MAIL_USE_TLS'):
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config.get('MAIL_SERVER'), app.config.get('MAIL_PORT')),
                fromaddr=app.config.get('MAIL_ADMINS')[0],
                toaddrs=app.config.get('MAIL_ADMINS'),
                subject='{} Failure'.format(app.config.get('APP_NAME')),
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('app has been created.')
    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config.get('LANGUAGES'))


from . import models  # NOQA
from . import beans  # NOQA

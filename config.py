import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    load_dotenv(os.path.join(basedir, '.env'))
    APP_NAME = os.environ.get('APP_NAME') or 'Flask Project'
    # python -c "import uuid; print(uuid.uuid4().hex)"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # flask_sqlalchemy
    DB_SERVER = os.environ.get('DB_SERVER')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_DATABASE = os.environ.get('DB_DATABASE')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT, DB_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {}
    # flask_mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_ADMINS = (os.environ.get('MAIL_ADMINS') or '').split(',')
    # flask_babel
    LANGUAGES = [
        'en',
        'zh',
        'zh_CN'
    ]
    # flask_docs
    API_DOC_MEMBER = [
        'api',
        'user'
    ]
    RESTFUL_API_DOC_EXCLUDE = []
    # flask_apsheduler
    SCHEDULER_API_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # flask_sqlalchemy
    DB_SERVER = os.environ.get('DB_SERVER')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_DATABASE_TEST = os.environ.get('DB_DATABASE_TEST')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT, DB_DATABASE_TEST)

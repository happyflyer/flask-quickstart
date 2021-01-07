from flask import Blueprint
bp = Blueprint('main', __name__)  # NOQA
from . import routes
from . import users
from .api import basedata as basedata_api
from .api import users as users_api

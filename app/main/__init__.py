from flask import Blueprint
bp = Blueprint('main', __name__)  # NOQA
from . import routes
from . import user_view
from .api import user_api

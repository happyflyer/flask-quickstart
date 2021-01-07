from flask import Blueprint
bp = Blueprint('auth', __name__)  # NOQA
from . import routes

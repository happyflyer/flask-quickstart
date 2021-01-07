from flask import Blueprint
bp = Blueprint('errors', __name__)  # NOQA
from . import handlers

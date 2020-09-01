# -*- coding: utf-8 -*-

from flask import Blueprint
bp = Blueprint('main_api', __name__)

from . import metadata
from . import users  # NOQA

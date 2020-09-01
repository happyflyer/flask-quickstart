# -*- coding: utf-8 -*-

from flask import Blueprint
bp = Blueprint('auth', __name__)

from . import routes  # NOQA

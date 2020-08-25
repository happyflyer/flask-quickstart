# -*- coding: utf-8 -*-

from flask import Blueprint


bp = Blueprint('api', __name__)
# api接口查询默认每页记录数
RECORDS_PER_PAGE = 25
# api接口查询每页最大记录数
RECORDS_MAX_PER_PAGE = 50

from .errors import error_response  # NOQA
from .errors import bad_request  # NOQA
from .errors import forbidden  # NOQA
from .errors import not_found  # NOQA

from .auth import basic_auth  # NOQA
from .auth import token_auth  # NOQA

from . import tokens  # NOQA

from ..main.api import users  # NOQA

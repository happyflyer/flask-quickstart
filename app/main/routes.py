# -*- coding: utf-8 -*-

from flask import redirect, url_for, render_template
from flask_babel import lazy_gettext as _l

from . import bp


@bp.route('/favicon.ico', methods=['GET'])
def favicon():
    return redirect(url_for('static', filename='logo/logo.png'))


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('main/index.jinja2', title=_l('Home'))

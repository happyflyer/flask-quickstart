# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_user, logout_user
from flask_babel import lazy_gettext as _l
from werkzeug.urls import url_parse

from ..models import User
from . import bp
from .forms import LoginForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """页面登录"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter(User.username == username).first()
        if user is None or not user.check_password(password):
            flash(_l('Invalid username or password!'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember_me)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('edit.jinja2', title=_l('Sign In'), form=form)


@bp.route('/logout', methods=['GET'])
def logout():
    """页面注销"""
    logout_user()
    return redirect(url_for('main.index'))

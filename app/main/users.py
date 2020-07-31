# -*- coding: utf-8 -*-

from flask import request, render_template, flash, redirect, url_for, abort
from flask_babel import lazy_gettext as _l
from flask_login import login_required, current_user

from .. import db, RECORDS_PER_PAGE, MODULES, PERMISSIONS, WRITE_PERMISSION, read_required, write_required
from ..models import User
from . import bp
from .forms import UserAddForm, UserGrantForm


@bp.route('/user', methods=['GET'])
@login_required
@write_required()
def list_users():
    page = request.args.get('page', 1, type=int)
    res = User.query.order_by(User.id.asc()).paginate(page, RECORDS_PER_PAGE, False)
    return render_template('main/user_list.jinja2', title=_l('User List'),
        res=res, page_target='main.list_users', modules=MODULES, permissions=PERMISSIONS)  # NOQA


@bp.route('/user/<string:username>', methods=['GET'])
@login_required
@read_required()
def get_user(username):
    # 访问他人主页时，需要main模块的W权限
    if current_user.username != username:
        if not current_user.check_permission('main', WRITE_PERMISSION):
            abort(403)
    user = User.query.filter(User.username == username).first_or_404()
    return render_template('main/user_item.jinja2', title=_l('User Profile'),
        user=user)  # NOQA


@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
@write_required()
def add_user():
    form = UserAddForm()
    if form.validate_on_submit():
        username = form.username.data
        # 用户名重复检查
        if User.query.filter(User.username == username).count() > 0:
            flash(_l('%(username)s already exists!', username=username))
            return redirect(url_for('main.add_user'))
        user = User.from_dict(form.data, new_user=True)
        db.session.add(user)
        db.session.commit()
        flash(_l('%(username)s has been added.', username=username))
        return redirect(url_for('main.list_users'))
    return render_template('edit.jinja2', title=_l('Add User'),
        form=form)  # NOQA


@bp.route('/user/<string:username>/grant', methods=['GET', 'POST'])
@login_required
@write_required()
def grant_permission(username):
    user = User.query.filter(User.username == username).first_or_404()
    form = UserGrantForm()
    if form.validate_on_submit():
        module = form.module.data
        permission = int(form.permission.data)
        # admin必须具有main模块的W权限
        if username == 'admin' and module == 'main' and permission < WRITE_PERMISSION:
            flash(_l('%(username)s must have %(permission)s to %(module)s!',
                username='admin', permission=PERMISSIONS[WRITE_PERMISSION], module='main'))  # NOQA
            return redirect(url_for('main.grant_permission', username=username))
        user.set_permission(module, permission)
        db.session.commit()
        flash(_l('%(username)s has been granted %(permission)s to %(module)s.',
            username=username, permission=PERMISSIONS[permission], module=module))  # NOQA
        return redirect(url_for('main.grant_permission', username=username))
    return render_template('edit.jinja2', title=_l('Grant User'),
        form=form)  # NOQA

from flask import request, render_template, flash, redirect, url_for, abort
from flask_babel import lazy_gettext as _l
from flask_login import login_required, current_user
from .. import db
from ..models import User
from ..modules import MODULES
from ..page import RECORDS_PER_PAGE
from ..permission import PERMISSIONS, WRITE_PERMISSION, read_required, write_required
from . import bp
from .forms import UserAddForm, UserGrantForm


@bp.route('/user', methods=['GET'])
@login_required
@write_required()
def list_users():
    username = request.args.get('username', None, type=str)
    custom_query = User.query
    if username is not None:
        custom_query = custom_query.filter(User.username.like('%' + username + '%'))
    page = request.args.get('page', 1, type=int)
    res = custom_query.order_by(User.id.asc()).paginate(page, RECORDS_PER_PAGE, False)
    return render_template('main/user_list.jinja2', title=_l('User List'),
        res=res,
        modules=MODULES,
        permissions=PERMISSIONS,
        keywords={
            "username": username if username else ''
        })  # NOQA


@bp.route('/user/<string:username>', methods=['GET'])
@login_required
@read_required()
def get_user(username):
    # 访问他人主页时，需要main模块的WRITE权限
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
            flash(_l('%(obj)s already exists!', obj=username))
            return redirect(url_for('main.add_user'))
        user = User.from_dict(form.data)
        if user:
            db.session.add(user)
            db.session.commit()
        flash(_l('%(obj)s has been added.', obj=username))
        return redirect(url_for('main.list_users'))
    return render_template('edit.jinja2', title=_l('Add User'),
        form=form)  # NOQA


@bp.route('/user/grant/<string:username>', methods=['GET', 'POST'])
@login_required
@write_required()
def grant_user(username):
    user = User.query.filter(User.username == username).first_or_404()
    form = UserGrantForm()
    if form.validate_on_submit():
        module = form.module.data
        permission = int(form.permission.data)
        # admin 必须具有 main 模块的 WRITE 权限
        if username == 'admin' and module == 'main' and permission < WRITE_PERMISSION:
            flash(_l('admin must have WRITE permission on main module!'))
            return redirect(url_for('main.grant_user', username=username))
        # 设置其他用户的权限
        user.set_permission(module, permission)
        db.session.commit()
        flash(_l('%(username)s has been granted %(pl)s permission on %(module)s.',
            username=username, pl=PERMISSIONS[permission], module=module))  # NOQA
        return redirect(url_for('main.grant_user', username=username, permission=permission))
    return render_template('edit.jinja2', title=_l('Grant User'),
        form=form)  # NOQA

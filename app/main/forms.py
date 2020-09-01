# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from .. import MODULES, PERMISSIONS
from ..models import User


class UserAddForm(FlaskForm):
    """新增用户表单"""
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Add'))

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError(_l('This username is already in use, Please change another username!'))


class UserGrantForm(FlaskForm):
    """用户授权表单"""
    module = SelectField(_l('Module'), validators=[DataRequired()], choices=[(m, m) for m in MODULES])  # NOQA
    permission = SelectField(_l('Permission'), validators=[DataRequired()], choices=[(str(p), PERMISSIONS[p]) for p in PERMISSIONS])  # NOQA
    submit = SubmitField(_l('Grant'))

    def __init__(self, *args, **kwargs):
        super(UserGrantForm, self).__init__(*args, **kwargs)

    def validate_module(self, module):
        if module.data not in MODULES:
            raise ValidationError(_l('Invalid module!'))

    def validate_permission(self, permission):
        if int(permission.data) not in PERMISSIONS:
            raise ValidationError(_l('Invalid permission!'))

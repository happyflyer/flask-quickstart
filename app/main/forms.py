from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from ..models import User
from ..modules import MODULES
from ..permission import PERMISSIONS


class UserAddForm(FlaskForm):
    username = StringField(_l('username'), validators=[DataRequired()])
    password = PasswordField(_l('password'), validators=[DataRequired()])
    password2 = PasswordField(_l('repeat password'), validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('add'))

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError(_l('this username is already in use!'))


class UserGrantForm(FlaskForm):
    module = SelectField(_l('module'), validators=[DataRequired()], choices=[
        (module, module) for module in MODULES])
    permission = SelectField(_l('permission'), validators=[
        DataRequired()], choices=[(str(p), PERMISSIONS[p]) for p in PERMISSIONS])
    submit = SubmitField(_l('grant'))

    def __init__(self, *args, **kwargs):
        super(UserGrantForm, self).__init__(*args, **kwargs)

    def validate_module(self, module):
        if module.data not in MODULES:
            raise ValidationError(_l('invalid module!'))

    def validate_permission(self, permission):
        if int(permission.data) not in PERMISSIONS:
            raise ValidationError(_l('invalid permission!'))

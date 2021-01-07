from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(_l('username'), validators=[DataRequired()])
    password = PasswordField(_l('password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('remember me'))
    submit = SubmitField(_l('sign in'))

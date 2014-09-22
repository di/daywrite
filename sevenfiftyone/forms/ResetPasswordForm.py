from flask import flash
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, EqualTo
from werkzeug import check_password_hash, generate_password_hash
from models import User


class ResetPasswordForm(Form):
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if self.password.data == self.confirm.data:
            return True
        return False


from flask import flash
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, EqualTo
from werkzeug import check_password_hash, generate_password_hash
from models import User

class ForgotPasswordForm(Form):
    email = TextField('Email address', [Required(), Email()])
    submit = SubmitField('Reset password')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if User.objects(email=self.email.data).first() is None:
            flash("This email address is not in the system.")
            return False
        return True

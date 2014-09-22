from flask import flash
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, EqualTo
from werkzeug import check_password_hash, generate_password_hash
from sevenfiftyone.models.User import User

class RegisterForm(Form):
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Choose a Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if User.objects(email=self.email.data).first() is not None:
            flash("This email address already has an account")
            return False
        if self.password.data != self.confirm.data:
            flash("Passwords must match")
            return False
        return True

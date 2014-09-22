from flask import flash
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, EqualTo
from werkzeug import check_password_hash, generate_password_hash
from sevenfiftyone.models.User import User


class LoginForm(Form):
    email = TextField('Email address', [Required()], description="Enter your email address")
    password = PasswordField('Password', [Required()], description="Password")
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        try:
            user = User.objects.get(email=self.email.data)
        except User.DoesNotExist:
            flash("This email address is not in the system.")
            return False

        if not user.confirmed:
            flash("Account not yet confirmed. Check your email. ")
            return False

        if not check_password_hash(user.password, self.password.data):
            flash("Invalid password, please try again.")
            return False

        self.user = user
        return True


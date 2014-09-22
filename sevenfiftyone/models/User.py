import bson
import datetime
from flask.ext.security import UserMixin
from mongoengine import *


class User(Document, UserMixin):
    id = ObjectIdField(
        primary_key=True,
        default=lambda: bson.ObjectId())
    email = EmailField(required=True)
    password = StringField(required=True)
    stripe_id = StringField()
    confirmed = BooleanField(default=False)
    confirmed_at = DateTimeField()
    registered = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now())
    email_hash = StringField()

    meta = {'allow_inheritance': True}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def activate(self):
        self.confirmed = True
        self.confirmed_at = datetime.datetime.now()
        self.save()

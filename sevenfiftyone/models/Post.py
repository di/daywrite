from mongoengine import *
from datetime import datetime
from User import User

class Post(Document):
    content = StringField(default="")
    date = DateTimeField(default=datetime.now)
    completed = BooleanField(default=False)
    date_string = StringField()
    blurb = StringField()
    length = IntField(default=0)
    owner = ReferenceField(User)

    def save(self, *args, **kwargs):
        self.date_string = self.date.strftime("%Y-%m-%d")
        super(Post, self).save(*args, **kwargs)

    def url_string(self):
        return self.date_string.replace("-","/")

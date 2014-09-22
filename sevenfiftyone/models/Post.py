from mongoengine import *
from datetime import datetime
from Status import Status

class Post(Document):
    content = StringField(default="")
    date = DateTimeField(default=datetime.now)
    completed = BooleanField(default=False)
    date_string = StringField(unique=True)
    past_status = ListField(EmbeddedDocumentField(Status))
    length = IntField(default=0)

    meta = {
        'indexes': ['date_string']
    }

    def save(self, *args, **kwargs):
        self.date_string = self.date.strftime("%Y-%m-%d")
        super(Post, self).save(*args, **kwargs)

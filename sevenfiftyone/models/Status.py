from mongoengine import *

class Status(EmbeddedDocument):
    date_string = StringField()
    completed = BooleanField()

    def url_string(self):
        return self.date_string.replace("-","/")

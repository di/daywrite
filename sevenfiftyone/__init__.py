#!/usr/bin/python

from datetime import datetime
from HTMLParser import HTMLParseError
import requests
import time
import os
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
from mongoengine import *
from urlparse import urlparse
from time import strptime, mktime, strftime
from datetime import datetime, timedelta
from mongoengine import Q
import re

app = Flask(__name__)

# Tell jinja to trim blocks
app.jinja_env.trim_blocks = True

def make_datestring(date=datetime.now()):
    return date.strftime("%Y-%m-%d")

def past_status(date):
    past_status = []
    for i in reversed(range(1, 32)):
        date_string = make_datestring(date - timedelta(days=i))
        try:
            post = Post.objects.get(date_string=date_string)
            past_status.append(Status(date_string=date_string, completed=post.completed))
        except Post.DoesNotExist:
            past_status.append(Status(date_string=date_string, completed=False))
    return past_status

@app.route("/", methods=["GET"])
def root():
    now = datetime.now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    try:
        post = Post.objects.get(Q(date__gt=start) & Q(date__lt=end))
    except Post.DoesNotExist:
        post = Post(date=now, past_status=past_status(now)).save()
    return render_template('index.html', post=post)

@app.route("/", methods=["POST"])
def post_root():
    content = request.form["content"]
    date_string = make_datestring()
    if request.form["date_string"] == date_string:
        length = len(re.findall(r'\b\w+\b', content))
        completed = length > 750
        Post.objects.get(date_string=date_string).update(set__content=request.form["content"], set__completed=completed, set__length=length)
        return "", 200
    return "", 500

@app.route("/<year>/<month>/<day>/", methods=["GET"])
def get_post(year, month, day):
    post = Post.objects.get(date_string="%s-%s-%s" % (year, month, day))
    return render_template('index.html', post=post)

class Status(EmbeddedDocument):
    date_string = StringField()
    completed = BooleanField()

    def url_string(self):
        return self.date_string.replace("-","/")

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

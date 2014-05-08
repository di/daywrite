#!/usr/bin/python

from datetime import datetime
from HTMLParser import HTMLParseError
import requests
import time
import os
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def root():
    d = datetime.today()
    date = "%d/%d/%d" % (d.month, d.day, d.year)
    return render_template('index.html', date=date)

@app.route("/day/<stringdate>")
def post(stringdate):
    d = datetime.strptime(stringdate, "%Y-%m-%d").date()
    date = d.strftime("%A %B %d, %Y")
    post = app.db.posts.find_one({'date': stringdate})
    return render_template('index.html', date=date, text=post['text'])

class Post:

    def __init__(self, date):
        self.date = date 
        self.content = ""

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()

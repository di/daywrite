#!/usr/bin/python

from HTMLParser import HTMLParseError
import requests
import time
import os
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify, session
from mongoengine import *
from urlparse import urlparse
from time import strptime, mktime, strftime
from datetime import datetime, timedelta
from mongoengine import Q
import re
from models.User import User
from models.Post import Post
from flask.ext.login import LoginManager, current_user, AnonymousUserMixin, login_user, logout_user
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from forms.ConfigureForm import ConfigureForm
import md5
from werkzeug import check_password_hash, generate_password_hash
from pytz import timezone

class AnonymousUser(AnonymousUserMixin):
  def __init__(self):
    self.admin = False

def make_datestring(date):
    ''' Takes in a date and makes it into the url-valid datestring. '''
    return date.strftime("%Y-%m-%d")

def make_text_date(date):
    ''' Takes in a date and makes it a human-readable datestring. '''
    return date.strftime("%b %-d, %Y")

def today():
    ''' Returns the current date for the current user. '''
    return datetime.now(timezone(current_user.timezone))

app = Flask(__name__)

# Session flags
@app.before_request
def func():
    session.permanent = True
    session.modified = True

# Set the session expiry to 5 minutes
app.permanent_session_lifetime = timedelta(minutes=5)

# Tell jinja to trim blocks
app.jinja_env.trim_blocks = True
app.jinja_env.globals.update(min=min)
app.jinja_env.filters["text_date"] = make_text_date

# For CSRF usage
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# For the blurb
punct = re.compile("\.|!|\?|;|:|,")

def past_status():
    post_map = dict()
    posts = Post.objects(owner=current_user.id).order_by('-date').limit(29)
    for post in posts:
        post_map[post.date_string] = (post.completed, post.length, post.url_string())
    return [post_map.get(make_datestring(today() - timedelta(days=i)), (False, 0, None)) for i in reversed(range(1,29))]

@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated():
        date_string = make_datestring(today())
        post, created = Post.objects.get_or_create(date_string=date_string, owner=current_user.id)
        return render_template('index.html', post=post, past_status=past_status(), user=current_user)
    return render_template('unauth_index.html')

@app.route("/invite/", methods=["POST"])
def post_invite():
    User.objects.get_or_create(email=request.form.get('email'))
    flash("Invite requested!")
    return redirect(url_for('index'))

@app.route("/login/", methods=["GET"])
def get_login():
    return render_template('login.html', form=LoginForm(), ref=request.args.get('next', None))

@app.route("/login/", methods=["POST"])
def post_login():
    form = LoginForm()
    ref = request.values.get('next', None)
    if form.validate_on_submit():
        # login and validate the user...
        user = User.objects.get(id=form.user.id)
        login_user(user)
        flash("Logged in successfully.")
        return redirect(ref or url_for("index"))
    return render_template("login.html", form=form, ref=ref)

@app.route("/", methods=["POST"])
def post_root():
    if not current_user.is_authenticated():
        return redirect(url_for("get_login"))

    content = request.form["content"]
    date_string = make_datestring(today())

    # Make sure the post is for the current day
    if request.form["date_string"] != date_string:
        # The post is not for the current day, trigger a refresh
        return jsonify({"completed":false, "refresh": True}), 200

    content = request.form["content"]

    # Count the number of words
    length = len(re.findall(r'\b\w+\b', content))
    completed = length > 750

    # Create the blurb
    blurb = content[:50]
    punct_result = punct.search(blurb)

    # See if there's any characters in the first 50 chars
    if punct_result is not None and 0 < punct_result.start() < 50:
        if punct_result.group() == "." :
            # There's a period, just keep it
            blurb = blurb[:punct_result.start()+1]
        else :
            # There's something else, remove it and add an elllipsis
            blurb = blurb[:punct_result.start()] + "..."
    else :
        # There's nothing, get the last space and replace it with an
        # ellipsis
        blurb = blurb[:blurb.rfind(" ")] + "..."

    # Save the post
    post = Post.objects.get(date_string=date_string, owner=current_user.id)
    post.update(set__content=content, set__completed=completed, set__length=length, set__blurb=blurb)

    # Check the user's archive flag
    if not current_user.has_archive:
        current_user.has_archive = True
        current_user.save()

    return jsonify({"completed":length > 750, "refresh": False}), 200

@app.route("/<int:year>/<int:month>/<int:day>/", methods=["GET"])
def get_post(year, month, day):
    if not current_user.is_authenticated():
        return redirect(url_for("index"))

    # Get the date string with leading zeros from the URL
    date_string = "%d-%02d-%02d" % (year, month, day)

    # If the archive is today, go to the index instead
    if date_string == make_datestring(today()):
        return redirect(url_for("index"))

    # See if the date in the URL corresponds to a post
    try:
        post = Post.objects.get(date_string=date_string, owner=current_user.id)
    except Post.DoesNotExist:
        return render_template('missing.html', date_string=date_string)

    return render_template('past_single.html', post=post)

@app.route("/past/", methods=["GET"])
def get_past():
    if not current_user.is_authenticated():
        return redirect(url_for("index"))

    posts = Post.objects(owner=current_user.id, length__gt=0).order_by('-date')
    return render_template('past.html', posts=posts)

@app.route("/register/", methods=["GET"])
def register():
    return render_template('register.html', form=RegisterForm())

@app.route("/register/", methods=["POST"])
def post_register():
    form = RegisterForm()
    if form.validate_on_submit():
        email_hash = md5.new(form.email.data.strip().lower()).hexdigest()
        user = User(email=form.email.data, email_hash=email_hash)
        user.password = generate_password_hash(form.password.data)
        user.registered = True

        '''
        # Create a stripe customer
        stripe.api_key = app.config['STRIPE_SECRET_KEY']
        customer = stripe.Customer.create(email=user.email)
        user.stripe_id = customer.id
        '''

        user.save()
        login_user(user)
        flash("Successfully registered")
        return redirect(url_for("index"))
    return render_template('register.html', form=RegisterForm())

@app.route("/configure/", methods=["GET"])
def get_configure():
    form = ConfigureForm()
    form.timezone.data = current_user.timezone
    return render_template('configure.html', form=form)

@app.route("/configure/", methods=["POST"])
def post_configure():
    return None

@app.route("/forgot_password/")
def forgot_password():
    return "Too bad."

@app.route("/logout/")
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("get_login"))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return User.objects.get(id=userid)
    except User.DoesNotExist:
        flash("This user account no longer exists.")
        return AnonymousUser()

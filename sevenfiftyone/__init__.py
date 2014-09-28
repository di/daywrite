#!/usr/bin/python

from HTMLParser import HTMLParseError
import requests
import time
import os
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
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
import md5
from werkzeug import check_password_hash, generate_password_hash
from pytz import timezone

class AnonymousUser(AnonymousUserMixin):
  def __init__(self):
    self.admin = False

def make_datestring(date):
    return date.strftime("%Y-%m-%d")

def make_text_date(date):
    return date.strftime("%b %-d, %Y")

app = Flask(__name__)

# Tell jinja to trim blocks
app.jinja_env.trim_blocks = True
app.jinja_env.globals.update(min=min)
app.jinja_env.filters["text_date"] = make_text_date

# For CSRF usage
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

def past_status():
    date = datetime.now(timezone(current_user.timezone))
    past_status = []
    for i in reversed(range(1, 30)):
        date_string = make_datestring(date - timedelta(days=i))
        try:
            post = Post.objects.get(date_string=date_string, owner=current_user.id)
            past_status.append((post.completed, post.length, post.url_string()))
        except Post.DoesNotExist:
            past_status.append((False, 0, None))
    return past_status

@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated():
        date_string = make_datestring(datetime.now(timezone(current_user.timezone)))
        post, created = Post.objects.get_or_create(date_string=date_string, owner=current_user.id)
        return render_template('index.html', post=post, past_status=past_status())
    return render_template('login.html', form=LoginForm(), ref=request.args.get('next', None))

@app.route("/", methods=["POST"])
def post_root():
    if current_user.is_authenticated():
        content = request.form["content"]
        date_string = make_datestring(datetime.now(timezone(current_user.timezone)))
        if request.form["date_string"] == date_string:
            content = request.form["content"]
            length = len(re.findall(r'\b\w+\b', content))
            completed = length > 750
            blurb = content[:50]
            if 0 < blurb.find(".") < 50:
                blurb = blurb[:blurb.find(".")+1]
            else :
                blurb = blurb[:blurb.rfind(" ")] + "..."
            Post.objects.get(date_string=date_string, owner=current_user.id).update(set__content=content, set__completed=completed, set__length=length, set__blurb=blurb)
            return jsonify({"completed":length > 750, "refresh": False}), 200
        return jsonify({"completed":false, "refresh": True}), 200
    else:
        form = LoginForm()
        ref = request.values.get('next', None)
        if form.validate_on_submit():
            # login and validate the user...
            user = User.objects.get(id=form.user.id)
            login_user(user)
            flash("Logged in successfully.")
            return redirect(ref or url_for("index"))
        return render_template("login.html", form=form, ref=ref)


@app.route("/<int:year>/<int:month>/<int:day>/", methods=["GET"])
def get_post(year, month, day):
    if current_user.is_authenticated():
        date_string = "%d-%02d-%02d" % (year, month, day)
        try:
            post = Post.objects.get(date_string=date_string, owner=current_user.id)
        except Post.DoesNotExist:
            return render_template('missing.html', date_string=date_string)
        return render_template('past_single.html', post=post)
    return redirect(url_for("index"))

@app.route("/past/", methods=["GET"])
def get_past():
    if current_user.is_authenticated():
        return render_template('past.html', posts=Post.objects(owner=current_user.id, length__gt=0).order_by('-date'))
    return redirect(url_for("index"))

@app.route("/register/", methods=["GET"])
def get_register():
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
    return render_template('register.html', form=RegisterForm())


@app.route("/forgot_password/")
def forgot_password():
    return "Too bad."

@app.route("/logout/")
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return User.objects.get(id=userid)
    except User.DoesNotExist:
        flash("This user account no longer exists.")
        return AnonymousUser()

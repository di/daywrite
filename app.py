import os
from flask import Flask
from urlparse import urlparse
from flask import Flask
from pymongo import Connection
import sevenfiftyone
from mongoengine import *
from flask.ext.mongoengine import MongoEngine


if __name__ == '__main__' :
    app = sevenfiftyone.app

    # MongoEngine configuration
    app.config["MONGODB_SETTINGS"] = {
        "DB": urlparse('MONGOHQ_URL').path[1:],
        "host": os.environ.get('MONGOHQ_URL')}

    # MongoEngine DB
    db = MongoEngine(app)

    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_debugger=True, use_reloader=True)

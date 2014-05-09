import os
from flask import Flask
from urlparse import urlparse
from flask import Flask
from pymongo import Connection
import sevenfiftyone

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
    # Get a connection
    connection = Connection(MONGO_URL)
    # Get the database
    db = connection[urlparse(MONGO_URL).path[1:]]
else :
    # Misconfigured
    pass

if __name__ == '__main__' :
    app = sevenfiftyone.app
    app.db = db
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_debugger=True, use_reloader=True)

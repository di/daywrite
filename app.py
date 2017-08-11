import os
from urlparse import urlparse
import sevenfiftyone
from flask.ext.mongoengine import MongoEngine


if __name__ == '__main__':
    app = sevenfiftyone.app

    # MongoEngine configuration
    app.config["MONGODB_SETTINGS"] = {
        "DB": urlparse('MONGODB_URI').path[1:],
        "host": os.environ.get('MONGODB_URI')}

    # MongoEngine DB
    db = MongoEngine(app)

    port = int(os.environ.get('PORT', 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        use_debugger=True,
        use_reloader=True,
    )

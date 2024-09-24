#!/usr/bin/python3
"""Flask app for returning API status
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_current_session(exception):
    """Removes current SQLAlchemy session"""
    if exception:
        print(exception)
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    import os

    host = os.environ.get('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = os.environ.get('HBNB_API_PORT')
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)

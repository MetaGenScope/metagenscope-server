"""MetaGenScope server application."""


import os
import datetime


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


from instance.config import app_config


# Instantiate the app
app = Flask(__name__)

# Set config
CONFIG_NAME = os.getenv('APP_SETTINGS', 'development')
app.config.from_object(app_config[CONFIG_NAME])

# Instantiate the DB
db = SQLAlchemy(app)


# User model
# pylint: disable=too-few-public-methods
class User(db.Model):
    """MetaGenScope User model."""

    __tablename__ = "users"
    # pylint: disable=invalid-name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email):
        """Initialize MetaGenScope User model."""
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.utcnow()


# Routes

@app.route('/ping', methods=['GET'])
def ping_pong():
    """Respond to ping."""
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

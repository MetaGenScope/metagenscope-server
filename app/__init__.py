"""MetaGenScope server application."""


import os


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


from app.config import app_config
from app.api.views import users_blueprint


# Instantiate the DB
db = SQLAlchemy()


def create_app():
    """Create and bootstrap app."""
    # Instantiate the app
    app = Flask(__name__)

    # Set config
    config_name = os.getenv('APP_SETTINGS', 'development')
    app.config.from_object(app_config[config_name])

    # Set up extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(users_blueprint)

    return app

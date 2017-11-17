"""MetaGenScope server application."""


import os


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


from app.config import app_config
from app.api.views import users_blueprint


# Instantiate extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    """Create and bootstrap app."""
    # Instantiate the app
    app = Flask(__name__)

    # Set config
    config_name = os.getenv('APP_SETTINGS', 'development')
    app.config.from_object(app_config[config_name])

    # Set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(users_blueprint)

    return app

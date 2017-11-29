"""MetaGenScope server application."""


import os


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS


from app.config import app_config
from app.extensions import db, migrate, bcrypt
from app.api.v1.ping import ping_blueprint
from app.api.v1.users import users_blueprint
from app.api.v1.auth import auth_blueprint
from app.api.v1.organizations import organizations_blueprint


def create_app():
    """Create and bootstrap app."""
    # Instantiate the app
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Set config
    config_name = os.getenv('APP_SETTINGS', 'development')
    app.config.from_object(app_config[config_name])

    # Set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(ping_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(organizations_blueprint, url_prefix='/api/v1')

    return app

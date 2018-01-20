"""MetaGenScope server application."""


import os


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS


from app.config import app_config
from app.extensions import mongoDB, db, migrate, bcrypt
from app.api.v1.ping import ping_blueprint
from app.api.v1.users import users_blueprint
from app.api.v1.auth import auth_blueprint
from app.api.v1.organizations import organizations_blueprint
from app.api.v1.query_results import query_results_blueprint
from app.api.v1.sample_groups import sample_groups_blueprint


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
    mongoDB.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register application components
    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_blueprints(app):
    """Register API endpoint blueprints for app."""
    app.register_blueprint(ping_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(organizations_blueprint, url_prefix='/api/v1')
    app.register_blueprint(query_results_blueprint, url_prefix='/api/v1')
    app.register_blueprint(sample_groups_blueprint, url_prefix='/api/v1')


def register_error_handlers(app):
    """Register JSON error handlers for app."""
    app.register_error_handler(404, page_not_found)


def page_not_found(not_found_error):
    """Handle 404 Not Found error."""
    return jsonify(error=404, text=str(not_found_error)), 404

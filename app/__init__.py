"""MetaGenScope server application."""

import os

from flask import Flask, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.api.v1.ping import ping_blueprint
from app.api.v1.users import users_blueprint
from app.api.v1.auth import auth_blueprint
from app.api.v1.organizations import organizations_blueprint
from app.api.v1.samples import samples_blueprint
from app.api.v1.sample_groups import sample_groups_blueprint
from app.api.constants import URL_PREFIX
from app.config import app_config
from app.display_modules import all_display_modules
from app.tool_results import all_tool_result_modules
from app.extensions import mongoDB, db, migrate, bcrypt


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
    register_tool_result_modules(app)
    register_display_modules(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_tool_result_modules(app):
    """Register each Tool Result module."""
    tool_result_modules_blueprint = Blueprint('tool_result_modules', __name__)
    for module in all_tool_result_modules:
        module.register_api_call(tool_result_modules_blueprint)
    app.register_blueprint(tool_result_modules_blueprint, url_prefix=URL_PREFIX)


def register_display_modules(app):
    """Register each Display Module."""
    display_modules_blueprint = Blueprint('display_modules', __name__)
    for module in all_display_modules:
        module.register_api_call(display_modules_blueprint)
    app.register_blueprint(display_modules_blueprint, url_prefix=URL_PREFIX)


def register_blueprints(app):
    """Register API endpoint blueprints for app."""
    app.register_blueprint(ping_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(users_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(auth_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(organizations_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(samples_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(sample_groups_blueprint, url_prefix=URL_PREFIX)


def register_error_handlers(app):
    """Register JSON error handlers for app."""
    app.register_error_handler(404, page_not_found)


def page_not_found(not_found_error):
    """Handle 404 Not Found error."""
    return jsonify(error=404, text=str(not_found_error)), 404

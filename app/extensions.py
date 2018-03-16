"""App extensions defined here to avoid cyclic imports."""

from celery import Celery

from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


mongoDB = MongoEngine()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

# Celery w/ Flask facory pattern from:
#   https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern
celery = Celery(__name__)  # pylint: disable=invalid-name

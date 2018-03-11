"""App extensions defined here to avoid cyclic imports."""

from celery import Celery

from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from app.config import Config


mongoDB = MongoEngine()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

# Celery w/ Flask facory pattern from:
#   https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)  # pylint: disable=invalid-name

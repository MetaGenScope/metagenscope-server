"""App extensions defined here to avoid cyclic imports."""

from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

mongoDB = MongoEngine()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

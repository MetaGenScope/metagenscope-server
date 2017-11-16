"""API model definitions."""


import datetime

from app import db


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

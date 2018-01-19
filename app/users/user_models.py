"""User model definitions."""

import datetime
import uuid
import jwt

from flask import current_app
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields, pre_load

from app.api.utils import uuid2slug
from app.extensions import db, bcrypt


# pylint: disable=invalid-name
users_organizations = db.Table(
    'users_organizations',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id')),
    db.Column('organization_id', UUID(as_uuid=True), db.ForeignKey('organizations.id')),
    db.Column('role', db.String(128), default='member', nullable=False)
)


class User(db.Model):
    """MetaGenScope User model."""

    __tablename__ = 'users'

    # pylint: disable=invalid-name
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    organizations = relationship(
        'Organization',
        secondary=users_organizations,
        back_populates='users')

    def __init__(
            self, username, email, password,
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.created_at = created_at

    @classmethod
    def encode_auth_token(cls, user_id):
        """Generate the auth token."""
        try:
            days = current_app.config.get('TOKEN_EXPIRATION_DAYS')
            seconds = current_app.config.get('TOKEN_EXPIRATION_SECONDS')
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=days, seconds=seconds),
                'iat': datetime.datetime.utcnow(),
                'sub': str(user_id)
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        # pylint: disable=broad-except
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decode the auth token - :param auth_token: - :return: UUID|string."""
        try:
            secret = current_app.config.get('SECRET_KEY')
            payload = jwt.decode(auth_token, secret)
            return uuid.UUID(payload['sub'])
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class UserSchema(Schema):
    """Serializer for User."""

    slug = fields.Str()
    username = fields.Str()
    email = fields.Str()

    @pre_load
    def slugify_id(self, in_data):
        in_data['slug'] = uuid2slug(in_data['id'])
        return in_data


user_schema = UserSchema()

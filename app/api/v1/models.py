"""API model definitions."""


import datetime
import uuid
import jwt

from flask import current_app
from sqlalchemy.dialects.postgresql import UUID
from flask_mongoengine.wtf import model_form

from app.extensions import mongoDB, db, bcrypt


# User model
class User(db.Model):
    """MetaGenScope User model."""

    __tablename__ = "users"

    # pylint: disable=invalid-name
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text("uuid_generate_v4()"))
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

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


# Organization model
# pylint: disable=too-few-public-methods
class Organization(db.Model):
    """MetaGenScope Organization model."""

    __tablename__ = "organizations"

    # pylint: disable=invalid-name
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text("uuid_generate_v4()"))
    name = db.Column(db.String(128), unique=True, nullable=False)
    adminEmail = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, adminEmail, created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope Organization model."""
        self.name = name
        self.adminEmail = adminEmail
        self.created_at = created_at


# Result model
class Result(mongoDB.Document):
    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False)
    sampleId = mongoDB.StringField()
    toolId = mongoDB.StringField()
    sampleName = mongoDB.StringField()

    meta = {'allow_inheritance': True}


# Metaphlan2 result model
class Metaphlan2Result(Result):
    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


# Shortbred result model
class ShortbredResult(Result):
    abundances = mongoDB.DictField()


# Mic Census result model
class MicCensusResult(Result):
    average_genome_size = mongoDB.IntField()
    total_bases = mongoDB.IntField()
    genome_equivalents = mongoDB.IntField()


# Kraken result model
class KrakenResult(Result):
    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


# Nanopore Taxa result model
class NanoporeTaxaResult(Result):
    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


# Reads Classified result model
class ReadsClassifiedResult(Result):
    viral = mongoDB.IntField()
    archaea = mongoDB.IntField()
    bacteria = mongoDB.IntField()
    host = mongoDB.IntField()
    unknown = mongoDB.IntField()


# Hmp Sites result model
class HmpSitesResult(Result):
    gut = mongoDB.IntField()
    skin = mongoDB.IntField()
    throat = mongoDB.IntField()


# Food Pet result model
class FoodPetResult(Result):
    vegetables = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    fruits = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    pets = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    meats = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    total_reads = mongoDB.IntField()

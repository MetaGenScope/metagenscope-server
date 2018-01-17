"""Environment configurations."""

# pylint: disable=too-few-public-methods

import os


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    MONGODB_HOST = os.environ.get('MONGODB_TEST_HOST')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""

    # Set these explicitly just to be extra safe
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')


# pylint: disable=invalid-name
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

"""Environment configurations."""

# pylint: disable=too-few-public-methods

import os


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True
    SECRET_KEY = 'my_precious'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = 'my_precious'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# pylint: disable=invalid-name
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

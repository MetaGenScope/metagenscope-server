"""Test suites for application configurations."""

import unittest

from flask import current_app
from flask_testing import TestCase

from app import app
from instance.config import app_config


class TestDevelopmentConfig(TestCase):
    """Test suite for development configuration."""

    def create_app(self):
        app.config.from_object(app_config['development'])
        return app

    def test_app_is_development(self):
        """Ensure appropriate configuration values for development environment."""
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgres://postgres:postgres@metagenscope-db:5432/users_dev'
        )


class TestTestingConfig(TestCase):
    """Test suite for testing configuration."""

    def create_app(self):
        app.config.from_object(app_config['testing'])
        return app

    def test_app_is_testing(self):
        """Ensure appropriate configuration values for testing environment."""
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgres://postgres:postgres@metagenscope-db:5432/users_test'
        )


class TestProductionConfig(TestCase):
    """Test suite for production configuration."""

    def create_app(self):
        app.config.from_object(app_config['production'])
        return app

    def test_app_is_production(self):
        """Ensure appropriate configuration values for production environment."""
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()

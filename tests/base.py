"""Defines base test suite to use for MetaGenScope tests."""

from flask_testing import TestCase

from app import create_app, db
from app.config import app_config


app = create_app()


class BaseTestCase(TestCase):
    """Base MetaGenScope test suite."""

    def create_app(self):
        """Create app configured for testing."""
        app.config.from_object(app_config['testing'])
        return app

    def setUp(self):
        """Set up test DB."""
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """Tear down test DB."""
        db.session.remove()
        db.drop_all()

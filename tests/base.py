"""Defines base test suite to use for MetaGenScope tests."""

import logging

from flask_testing import TestCase

from app import create_app, db
from app.config import app_config
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample


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

        # Disable logging
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        """Tear down test DBs."""
        # Postgres
        db.session.remove()
        db.drop_all()

        # Mongo
        AnalysisResultMeta.drop_collection()
        Sample.drop_collection()

        # Enable logging
        logging.disable(logging.NOTSET)

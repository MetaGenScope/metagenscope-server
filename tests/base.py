"""Defines base test suite to use for MetaGenScope tests."""

import logging
import json

from flask_testing import TestCase

from app import create_app, db, celery, update_celery_settings
from app.config import app_config
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample


app = create_app()


class BaseTestCase(TestCase):
    """Base MetaGenScope test suite."""

    def create_app(self):
        """Create app configured for testing."""
        config_cls = app_config['testing']
        app.config.from_object(config_cls)
        update_celery_settings(celery, config_cls)
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

    def verify_analysis_result(self, analysis_result, name):
        """Verify an analysis result was created succesfully."""
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.uuid}/{name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'S')
            self.assertIn('samples', data['data']['data'])

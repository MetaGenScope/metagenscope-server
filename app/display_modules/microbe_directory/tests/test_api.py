"""Test suite for Microbe Directory result type."""

import json

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.microbe_directory.tests.factory import MicrobeDirectoryFactory

from tests.base import BaseTestCase


class TestMicrobeDirectoryModule(BaseTestCase):
    """Test suite for Microbe Directory result type."""

    def test_get_microbe_directory(self):
        """Ensure getting a single Microbe Directory behaves correctly."""
        microbe_directory = MicrobeDirectoryFactory()
        wrapper = AnalysisResultWrapper(data=microbe_directory, status='S')
        analysis_result = AnalysisResultMeta(microbe_directory=wrapper).save()
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.uuid}/microbe_directory',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'S')
            self.assertIn('samples', data['data']['data'])

"""Helper functions for display module tests."""
import json

from app import db
from app.analysis_results.analysis_result_models import (
    AnalysisResultMeta,
    AnalysisResultWrapper
)
from tests.base import BaseTestCase
from tests.utils import add_sample_group


class BaseDisplayModuleTest(BaseTestCase):
    """Helper functions for display module tests."""

    def generic_getter_test(self, data, endpt):
        """Check that we can get an analysis result."""
        wrapper = AnalysisResultWrapper(data=data, status='S')
        analysis_result = AnalysisResultMeta(**{endpt: wrapper}).save()
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.uuid}/{endpt}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'S')
            self.assertIn('samples', data['data']['data'])

    def generic_adder_test(self, data, endpt):
        """Check that we can add an analysis result."""
        wrapper = AnalysisResultWrapper(data=data)
        result = AnalysisResultMeta(**{endpt: wrapper}).save()
        self.assertTrue(result.uuid)
        self.assertTrue(getattr(result, endpt))

    def generic_run_group_test(self, sample_builder, wrangler, endpt):
        """Check that we can run a wrangler on a set of samples."""
        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [sample_builder(i) for i in range(6)]
        db.session.commit()
        wrangler.run_sample_group(sample_group.id).get()
        analysis_result = sample_group.analysis_result
        self.assertIn(endpt, analysis_result)
        wrangled = getattr(analysis_result, endpt)
        self.assertEqual(wrangled.status, 'S')

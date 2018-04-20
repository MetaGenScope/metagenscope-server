"""Helper functions for display module tests."""

import json

from app import db
from app.analysis_results.analysis_result_models import (
    AnalysisResultMeta,
    AnalysisResultWrapper
)
from tests.base import BaseTestCase
from tests.utils import add_sample_group, add_sample


class BaseDisplayModuleTest(BaseTestCase):
    """Helper functions for display module tests."""

    def generic_getter_test(self, data, endpt, verify_fields=('samples',)):
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
            analysis_result = data['data']
            self.assertEqual(analysis_result['status'], 'S')
            for field in verify_fields:
                self.assertIn(field, analysis_result['data'])

    def generic_adder_test(self, data, endpt):
        """Check that we can add an analysis result."""
        wrapper = AnalysisResultWrapper(data=data)
        result = AnalysisResultMeta(**{endpt: wrapper}).save()
        self.assertTrue(result.uuid)
        self.assertTrue(getattr(result, endpt))

    def generic_run_sample_test(self, sample_kwargs, wrangler, endpt):
        """Check that we can run a wrangler on a single samples."""
        sample = add_sample(name='Sample01', sample_kwargs=sample_kwargs)
        db.session.commit()
        wrangler.help_run_sample(sample.id, endpt).get()
        analysis_result = sample.analysis_result.fetch()
        self.assertIn(endpt, analysis_result)
        wrangled_sample = getattr(analysis_result, endpt)
        self.assertEqual(wrangled_sample.status, 'S')

    def generic_run_group_test(self, sample_builder, wrangler, endpt):
        """Check that we can run a wrangler on a set of samples."""
        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [sample_builder(i) for i in range(6)]
        db.session.commit()
        wrangler.help_run_sample_group(sample_group.id, endpt).get()
        analysis_result = sample_group.analysis_result
        self.assertIn(endpt, analysis_result)
        wrangled = getattr(analysis_result, endpt)
        self.assertEqual(wrangled.status, 'S')

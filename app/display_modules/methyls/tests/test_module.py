"""Test suite for Methyls diplay module."""
import json

from app import db
from app.display_modules.methyls.wrangler import MethylWrangler
from app.samples.sample_models import Sample
from app.analysis_results.analysis_result_models import (
    AnalysisResultMeta,
    AnalysisResultWrapper
)
from app.display_modules.methyls import MethylResult
from app.display_modules.methyls.tests.factory import (
    MethylsFactory,
    create_one_sample
)
from app.tool_results.methyltransferases.tests.factory import create_methyls
from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestMethylsModule(BaseTestCase):
    """Test suite for Methyls diplay module."""

    def test_get_methyls(self):
        """Ensure getting a single Methyl behaves correctly."""
        methyls = MethylsFactory()
        wrapper = AnalysisResultWrapper(data=methyls, status='S')
        analysis_result = AnalysisResultMeta(methyltransferases=wrapper).save()
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.uuid}/methyltransferases',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'S')
            self.assertIn('samples', data['data']['data'])

    def test_add_methyls(self):
        """Ensure Methyl model is created correctly."""
        samples = {
            'test_sample_1': create_one_sample(),
            'test_sample_2': create_one_sample()
        }
        methyls_result = MethylResult(samples=samples)
        wrapper = AnalysisResultWrapper(data=methyls_result)
        result = AnalysisResultMeta(methyltransferases=wrapper).save()
        self.assertTrue(result.uuid)
        self.assertTrue(result.methyltransferases)

    def test_run_methyls_sample_group(self):  # pylint: disable=invalid-name
        """Ensure methyls run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            metadata = {'foobar': f'baz{i}'}
            data = create_methyls()
            return Sample(name=f'Sample{i}',
                          metadata=metadata,
                          methyltransferases=data).save()

        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [create_sample(i) for i in range(6)]
        db.session.commit()
        MethylWrangler.run_sample_group(sample_group.id).get()
        analysis_result = sample_group.analysis_result
        self.assertIn('methyltransferases', analysis_result)
        methyls = analysis_result.methyltransferases
        self.assertEqual(methyls.status, 'S')

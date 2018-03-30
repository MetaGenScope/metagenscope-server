"""Test suite for Microbe Directory Wrangler."""

from app import db
from app.display_modules.methyls.wrangler import MethylWrangler
from app.samples.sample_models import Sample
from app.tool_results.methyls.tests.factory import create_methyls

from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestMethylWrangler(BaseTestCase):
    """Test suite for Microbe Directory Wrangler."""

    def test_run_methyls_sample_group(self):  # pylint: disable=invalid-name
        """Ensure run_sample_group produces correct results."""

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

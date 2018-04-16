"""Test suite for Sample Similarity Wrangler."""

from app import db
from app.display_modules.sample_similarity.wrangler import SampleSimilarityWrangler
from app.samples.sample_models import Sample
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.kraken.tests.factory import create_kraken
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.metaphlan2.tests.factory import create_metaphlan2

from tests.base import BaseTestCase
from tests.utils import add_sample_group


KRAKEN_NAME = KrakenResultModule.name()
METAPHLAN2_NAME = Metaphlan2ResultModule.name()


class TestSampleSimilarityWrangler(BaseTestCase):
    """Test suite for Sample Similarity Wrangler."""

    def test_run_sample_group(self):
        """Ensure run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            metadata = {'foobar': f'baz{i}'}
            sample_data = {
                'name': f'Sample{i}',
                'metadata': metadata,
                KRAKEN_NAME: create_kraken(),
                METAPHLAN2_NAME: create_metaphlan2(),
            }
            return Sample(**sample_data).save()

        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [create_sample(i) for i in range(6)]
        db.session.commit()
        SampleSimilarityWrangler.run_sample_group(sample_group.id).get()
        analysis_result = sample_group.analysis_result
        self.assertIn('sample_similarity', analysis_result)
        sample_similarity = analysis_result.sample_similarity
        self.assertEqual(sample_similarity.status, 'S')
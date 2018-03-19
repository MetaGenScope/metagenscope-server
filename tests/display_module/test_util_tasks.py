"""Test suite for Display Module utility tasks."""

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.sample_similarity.tests.sample_similarity_factory import (
    create_mvp_sample_similarity,
)
from app.display_modules.utils import (
    categories_from_metadata,
    fetch_samples,
    persist_result,
    collate_samples,
)
from app.samples.sample_models import Sample
from app.tool_results.kraken.tests.kraken_factory import create_kraken

from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestDisplayModuleUtilityTasks(BaseTestCase):
    """Test suite for Display Module utility tasks."""

    def test_categories_from_metadata(self):
        """Ensure categories_from_metadata task works."""
        metadata1 = {
            'valid_category': 'foo',
            'invalid_category': 'bar',
        }
        metadata2 = {
            'valid_category': 'baz',
        }
        sample1 = Sample(name='Sample01', metadata=metadata1).save()
        sample2 = Sample(name='Sample02', metadata=metadata2).save()
        result = categories_from_metadata.delay([sample1, sample2]).get()
        self.assertEqual(1, len(result.keys()))
        self.assertNotIn('invalid_category', result)
        self.assertIn('valid_category', result)
        self.assertIn('foo', result['valid_category'])
        self.assertIn('baz', result['valid_category'])

    def test_fetch_samples(self):
        """Ensure fetch_samples task works."""
        sample1 = Sample(name='Sample01').save()
        sample2 = Sample(name='Sample02').save()
        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [sample1, sample2]
        db.session.commit()

        result = fetch_samples.delay(sample_group.id).get()
        self.assertIn(sample1, result)
        self.assertIn(sample2, result)

    def test_persist_result(self):
        """Ensure persist_result task works as intended."""
        wrapper = AnalysisResultWrapper()
        analysis_result = AnalysisResultMeta(sample_similarity=wrapper).save()
        sample_similarity = create_mvp_sample_similarity()

        persist_result.delay(sample_similarity,
                             analysis_result.uuid,
                             'sample_similarity').get()
        analysis_result.reload()
        self.assertIn('sample_similarity', analysis_result)
        self.assertIn('status', analysis_result['sample_similarity'])
        self.assertEqual('S', analysis_result['sample_similarity']['status'])

    def test_collate_samples(self):
        """Ensure collate_samples task works."""
        sample1 = Sample(name='Sample01', kraken=create_kraken()).save()
        sample2 = Sample(name='Sample02', kraken=create_kraken()).save()
        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [sample1, sample2]
        db.session.commit()

        result = collate_samples.delay('kraken', ['taxa'], sample_group.id).get()
        self.assertIn('Sample01', result)
        self.assertIn('Sample02', result)
        self.assertIn('taxa', result['Sample01'])
        self.assertIn('taxa', result['Sample02'])

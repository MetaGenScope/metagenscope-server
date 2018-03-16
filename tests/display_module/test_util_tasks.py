"""Test suite for Display Module utility tasks."""

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.sample_similarity.tests.sample_similarity_factory import (
    create_mvp_sample_similarity,
)
from app.display_modules.utils import fetch_samples, persist_result
from app.samples.sample_models import Sample

from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestDisplayModuleUtilityTasks(BaseTestCase):
    """Test suite for Display Module utility tasks."""

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

        persist_result.delay(analysis_result.uuid,
                             'sample_similarity',
                             sample_similarity).get()
        analysis_result.reload()
        self.assertIn('sample_similarity', analysis_result)

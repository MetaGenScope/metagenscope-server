"""Test suite for Sample Similarity tasks."""

from app.display_modules.sample_similarity.sample_similarity_tasks import (
    get_clean_samples,
    run_tsne,
)
from app.tool_results.kraken.tests.kraken_factory import create_kraken

from tests.base import BaseTestCase


class TestSampleSimilarityTasks(BaseTestCase):
    """Test suite for Sample Similarity tasks."""

    def test_clean_samples(self):
        """Ensure get_clean_samples method adds missing features to all samples."""
        sample_dict = {f'SMPL_{i}': create_kraken().taxa for i in range(3)}

        all_feature_ids = set([])
        for feature_set in sample_dict.values():
            all_feature_ids |= set(feature_set.keys())

        result = get_clean_samples(sample_dict, no_zero_features=False)

        for feature_set in result.values():
            for feature_id in all_feature_ids:
                self.assertIn(feature_id, feature_set)

    def test_clean_zeroed_samples(self):
        """Ensure get_clean_samples method removes features below threshold."""
        sample_dict = {f'SMPL_{i}': dict(create_kraken().taxa) for i in range(3)}
        sample_dict['SMPL_1']['somebadkingdom'] = 0.0000001

        all_feature_ids = set([])
        for feature_set in sample_dict.values():
            all_feature_ids |= set(feature_set.keys())

        result = get_clean_samples(sample_dict)

        for feature_set in result.values():
            self.assertNotIn('somebadkingdom', feature_set)

    def test_tsne_returns_data(self):
        """Ensure run_tsne method removes features below threshold."""
        sample_dict = {f'SMPL_{i}': dict(create_kraken().taxa) for i in range(3)}
        tsne_output = run_tsne(sample_dict)
        self.assertEqual((3, 2), tsne_output.shape)

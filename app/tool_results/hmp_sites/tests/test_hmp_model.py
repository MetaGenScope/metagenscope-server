"""Test suite for HMP Sites tool result model."""

from mongoengine import ValidationError

from app.samples.sample_models import Sample
from app.tool_results.hmp_sites import HmpSitesResult
from app.tool_results.hmp_sites.tests.constants import TEST_HMP

from tests.base import BaseTestCase


class TestHmpSitesModel(BaseTestCase):
    """Test suite for HMP Sites tool result model."""

    def test_add_hmp_sites_result(self):
        """Ensure HMP Sites result model is created correctly."""
        hmp_sites = HmpSitesResult(**TEST_HMP)
        sample = Sample(name='SMPL_01', hmp_sites=hmp_sites).save()
        self.assertTrue(sample.hmp_sites)
        tool_result = sample.hmp_sites
        self.assertEqual(len(tool_result), 5)
        self.assertEqual(tool_result['gut'], 0.6)
        self.assertEqual(tool_result['skin'], 0.3)
        self.assertEqual(tool_result['throat'], 0.25)
        self.assertEqual(tool_result['urogenital'], 0.7)
        self.assertEqual(tool_result['airways'], 0.1)

    def test_add_partial_sites_result(self):
        """Ensure HMP Sites result model accepts missing optional fields."""
        partial_hmp = dict(TEST_HMP)
        partial_hmp.pop('gut', None)
        hmp_sites = HmpSitesResult(**partial_hmp)
        sample = Sample(name='SMPL_01', hmp_sites=hmp_sites).save()
        self.assertTrue(sample.hmp_sites)
        tool_result = sample.hmp_sites
        self.assertEqual(len(tool_result), 5)
        self.assertEqual(tool_result['gut'], None)
        self.assertEqual(tool_result['skin'], 0.3)
        self.assertEqual(tool_result['throat'], 0.25)
        self.assertEqual(tool_result['urogenital'], 0.7)
        self.assertEqual(tool_result['airways'], 0.1)

    def test_add_malformed_hmp_sites_result(self):      # pylint: disable=invalid-name
        """Ensure validation fails for value outside of [0,1]."""
        bad_hmp = dict(TEST_HMP)
        bad_hmp['gut'] = 1.5
        hmp_sites = HmpSitesResult(**bad_hmp)
        sample = Sample(name='SMPL_01', hmp_sites=hmp_sites)
        self.assertRaises(ValidationError, sample.save)

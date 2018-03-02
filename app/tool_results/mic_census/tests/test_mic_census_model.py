"""Test suite for Microbe Census tool result model."""

from mongoengine import ValidationError

from app.samples.sample_models import Sample
from app.tool_results.mic_census import MicCensusResult
from app.tool_results.mic_census.tests.constants import TEST_CENSUS

from tests.base import BaseTestCase


class TestMicCensusResultModel(BaseTestCase):
    """Test suite for Microbe Census tool result model."""

    def test_add_hmp_sites_result(self):
        """Ensure Microbe Census result model is created correctly."""
        mic_census = MicCensusResult(**TEST_CENSUS)
        sample = Sample(name='SMPL_01', mic_census=mic_census).save()
        self.assertTrue(sample.mic_census)
        tool_result = sample.mic_census
        self.assertEqual(len(tool_result), 3)
        self.assertEqual(tool_result['average_genome_size'], 3)
        self.assertEqual(tool_result['total_bases'], 5)
        self.assertEqual(tool_result['genome_equivalents'], 250)

    def test_add_result_missing_fields(self):
        """Ensure validation fails if missing field."""
        partial_mic_census = dict(TEST_CENSUS)
        partial_mic_census.pop('average_genome_size', None)
        mic_census = MicCensusResult(**partial_mic_census)
        sample = Sample(name='SMPL_01', mic_census=mic_census)
        self.assertRaises(ValidationError, sample.save)

    def test_add_negative_value(self):
        """Ensure validation fails for negative values."""
        bad_mic_census = dict(TEST_CENSUS)
        bad_mic_census['average_genome_size'] = -3
        mic_census = MicCensusResult(**bad_mic_census)
        sample = Sample(name='SMPL_01', mic_census=mic_census)
        self.assertRaises(ValidationError, sample.save)

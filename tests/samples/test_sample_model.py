"""Test suite for Sample model."""

from mongoengine.errors import NotUniqueError

from app.samples.sample_models import Sample
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.kraken.tests.factory import create_kraken
from tests.base import BaseTestCase


KRAKEN_NAME = KrakenResultModule.name()


class TestSampleModel(BaseTestCase):
    """Test suite for Sample model."""

    def test_add_sample(self):
        """Ensure sample model is created correctly."""
        sample = Sample(name='SMPL_01', metadata={'subject_group': 1}).save()
        self.assertTrue(sample.id)
        self.assertTrue(sample.uuid)
        self.assertEqual(sample.name, 'SMPL_01')
        self.assertEqual(sample.metadata, {'subject_group': 1})
        self.assertTrue(sample.created_at)

    def test_add_duplicate_name(self):
        """Ensure duplicate sample names are not allowed."""
        Sample(name='SMPL_01').save()
        duplicate = Sample(name='SMPL_01')
        self.assertRaises(NotUniqueError, duplicate.save)

    def test_tool_result_names(self):
        """Ensure tool_result_names property works as expected."""
        sample_data = {'name': 'SMPL_01', KRAKEN_NAME: create_kraken()}
        sample = Sample(**sample_data).save()
        self.assertEqual(len(sample.tool_result_names), 1)
        self.assertIn(KRAKEN_NAME, sample.tool_result_names)

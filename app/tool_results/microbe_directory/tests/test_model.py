"""Test suite for Microbe Directory tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.microbe_directory import MicrobeDirectoryResult

from tests.base import BaseTestCase

from .constants import TEST_DIRECTORY


class TestMicrobeDirectoryModel(BaseTestCase):
    """Test suite for Microbe Directory tool result model."""

    def test_add_microbe_directory(self):
        """Ensure Microbe Directory result model is created correctly."""

        microbe_directory = MicrobeDirectoryResult(**TEST_DIRECTORY)
        sample = Sample(name='SMPL_01', microbe_directory_annotate=microbe_directory).save()
        self.assertTrue(sample.microbe_directory_annotate)

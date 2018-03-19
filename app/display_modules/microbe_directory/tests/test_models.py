"""Test suite for Microbe Directory model."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.microbe_directory.models import MicrobeDirectoryResult
from app.tool_results.microbe_directory.tests.factory import create_values

from tests.base import BaseTestCase


class TestMicrobeDirectoryResult(BaseTestCase):
    """Test suite for Microbe Directory model."""

    def test_add_microbe_directory(self):
        """Ensure Microbe Directory model is created correctly."""
        samples = create_values()
        microbe_directory_result = MicrobeDirectoryResult(samples=samples)
        wrapper = AnalysisResultWrapper(data=microbe_directory_result)
        result = AnalysisResultMeta(microbe_directory=wrapper).save()
        self.assertTrue(result.uuid)
        self.assertTrue(result.microbe_directory)

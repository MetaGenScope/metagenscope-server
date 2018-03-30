"""Test suite for Methyls model."""

from app.analysis_results.analysis_result_models import (
    AnalysisResultMeta,
    AnalysisResultWrapper
)
from app.display_modules.methyls.models import MethylResult
from tests.base import BaseTestCase
from .factory import create_values


class TestMethylsResult(BaseTestCase):
    """Test suite for Microbe Directory model."""

    def test_add_methyls(self):
        """Ensure Microbe Directory model is created correctly."""
        samples = create_values()
        methyls_result = MethylResult(samples=samples)
        wrapper = AnalysisResultWrapper(data=methyls_result)
        result = AnalysisResultMeta(methyltransferases=wrapper).save()
        self.assertTrue(result.uuid)
        self.assertTrue(result.methyltransferases)

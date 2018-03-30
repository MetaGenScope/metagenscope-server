"""Test suite for Methyls result type."""

from app.analysis_results.analysis_result_models import (
    AnalysisResultMeta,
    AnalysisResultWrapper
)
from app.display_modules.methyls.tests.factory import MethylsFactory

from tests.base import BaseTestCase


class TestMicrobeDirectoryModule(BaseTestCase):
    """Test suite for Microbe Directory result type."""

    def test_get_methyls(self):
        """Ensure getting a single Microbe Directory behaves correctly."""
        methyls = MethylsFactory()
        wrapper = AnalysisResultWrapper(data=methyls, status='S')
        analysis_result = AnalysisResultMeta(methyltransferases=wrapper).save()
        self.verify_analysis_result(analysis_result, 'methyltransferases')

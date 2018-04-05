"""Test suite for HMP Sites tool result uploads."""

from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestHmpSitesUploads(BaseToolResultTest):
    """Test suite for HMP Sites tool result uploads."""

    def test_upload_hmp_sites(self):
        """Ensure a raw HMP Sites tool result can be uploaded."""
        self.generic_test_upload(create_values(), 'hmp_sites')

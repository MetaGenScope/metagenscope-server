"""Test suite for Humann2 Normalize tool result model."""

from app.tool_results.humann2_normalize.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values, create_humann2_normalize


class TestHumann2NormalizeModel(BaseToolResultTest):
    """Test suite for Humann2 Normalize tool result model."""

    def test_add_humann2_normalize(self):
        """Ensure Humann2 Normalize tool result model is created correctly."""
        hum_norm = create_humann2_normalize()
        self.generic_add_sample_tool_test(hum_norm, MODULE_NAME)

    def test_upload_humann2_normalize(self):
        """Ensure a raw Humann2 Normalize tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)

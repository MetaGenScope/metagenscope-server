"""Test suite for Kraken tool result model."""

from app.tool_results.kraken.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values, create_kraken


class TestKrakenModel(BaseToolResultTest):
    """Test suite for Kraken tool result model."""

    def test_add_kraken(self):
        """Ensure Kraken tool result model is created correctly."""
        macrobes = create_kraken()
        self.generic_add_sample_tool_test(macrobes, MODULE_NAME)

    def test_upload_kraken(self):
        """Ensure a raw Kraken tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)

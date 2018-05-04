"""Test suite for Metaphlan2 tool result model."""

from app.tool_results.macrobes.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values, create_metaphlan2


class TestMetaphlan2Model(BaseToolResultTest):
    """Test suite for Metaphlan2 tool result model."""

    def test_add_krakenhll(self):
        """Ensure Metaphlan2 tool result model is created correctly."""
        mphlan2 = create_metaphlan2()
        self.generic_add_sample_tool_test(mphlan2, MODULE_NAME)

    def test_upload_krakenhll(self):
        """Ensure a raw Metaphlan2 tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)

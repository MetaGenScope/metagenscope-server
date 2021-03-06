"""Test suite for KrakenHLL tool result model."""

from app.tool_results.krakenhll.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values, create_krakenhll


class TestKrakenHLLModel(BaseToolResultTest):
    """Test suite for KrakenHLL tool result model."""

    def test_add_krakenhll(self):
        """Ensure KrakenHLL tool result model is created correctly."""
        macrobes = create_krakenhll()
        self.generic_add_sample_tool_test(macrobes, MODULE_NAME)

    def test_upload_krakenhll(self):
        """Ensure a raw KrakenHLL tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)

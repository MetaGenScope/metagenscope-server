"""Test suite for Macrobe tool result model."""

from app.tool_results.macrobes import MacrobeToolResult
from app.tool_results.macrobes.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestMacrobeModel(BaseToolResultTest):
    """Test suite for Macrobe tool result model."""

    def test_add_macrobes(self):
        """Ensure Macrobe tool result model is created correctly."""
        macrobes = MacrobeToolResult(**create_values())
        self.generic_add_test(macrobes, MODULE_NAME)

    def test_upload_macrobes(self):
        """Ensure a raw Macrobe tool result can be uploaded."""
        self.generic_test_upload(create_values(), MODULE_NAME)

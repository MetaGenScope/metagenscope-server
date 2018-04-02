"""Test suite for VFDB tool result model."""
from app.tool_results.vfdb import VFDBToolResult
from app.tool_results.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestVFDBModel(BaseToolResultTest):
    """Test suite for VFDB tool result model."""

    def test_add_vfdb(self):
        """Ensure VFDB tool result model is created correctly."""

        vfdbs = VFDBToolResult(**create_values())
        self.generic_add_test(vfdbs, 'vfdb_quantify')

    def test_upload_vfdb(self):
        """Ensure a raw Methyl tool result can be uploaded."""

        self.generic_test_upload(create_values(),
                                 'vfdb_quantify')

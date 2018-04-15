"""CARD AMR Alignment tool module."""

from app.tool_results.tool_module import ToolResultModule

from .constants import MODULE_NAME
from .models import CARDAMRToolResult


class CARDAMRResultModule(ToolResultModule):
    """CARD AMR Alignment tool module."""

    @classmethod
    def name(cls):
        """Return CARD AMR Alignment module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return CARD AMR Alignment module's model class."""
        return CARDAMRToolResult

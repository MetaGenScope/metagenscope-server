"""Humann2 Normalize tool module."""

from app.tool_results.tool_module import ToolResultModule

from .constants import MODULE_NAME
from .models import Humann2NormalizeToolResult


class VFDBResultModule(ToolResultModule):
    """Humann2 Normalize tool module."""

    @classmethod
    def name(cls):
        """Return Humann2 Normalize module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Humann2 Normalize module's model class."""
        return Humann2NormalizeToolResult

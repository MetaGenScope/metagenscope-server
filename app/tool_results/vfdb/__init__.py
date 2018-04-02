"""Virulence Factor tool module."""

from app.tool_results.tool_module import ToolResultModule

from .models import VFDBToolResult


class VFDBResultModule(ToolResultModule):
    """Virulence Factor tool module."""

    @classmethod
    def name(cls):
        """Return Virulence Factor module's unique identifier string."""
        return 'vfdb_quantify'

    @classmethod
    def result_model(cls):
        """Return Virulence Factor module's model class."""
        return VFDBToolResult

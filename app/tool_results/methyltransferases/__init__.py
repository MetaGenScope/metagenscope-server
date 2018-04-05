"""Methyltransferase tool module."""

from app.tool_results.tool_module import ToolResultModule

from .models import MethylToolResult


class MethylResultModule(ToolResultModule):
    """Methyltransferase tool module."""

    @classmethod
    def name(cls):
        """Return Methyltransferase module's unique identifier string."""
        return 'align_to_methyltransferases'

    @classmethod
    def result_model(cls):
        """Return Methyltransferase module's model class."""
        return MethylToolResult

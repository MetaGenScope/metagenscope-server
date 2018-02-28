"""Metaphlan 2 tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class Metaphlan2Result(ToolResult):
    """Metaphlan 2 tool's result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


class Metaphlan2ResultModule(ToolResultModule):
    """Metaphlan 2 tool module."""

    @classmethod
    def name(cls):
        """Return Metaphlan 2 module's unique identifier string."""
        return 'metaphlan2'

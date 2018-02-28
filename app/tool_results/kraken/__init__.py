"""Kraken tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class KrakenResult(ToolResult):
    """Kraken tool's result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


class KrakenResultModule(ToolResultModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return 'kraken'

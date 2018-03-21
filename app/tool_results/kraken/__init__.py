"""Kraken tool module."""

from app.tool_results.tool_module import ToolResultModule

from .models import KrakenResult


class KrakenResultModule(ToolResultModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return 'kraken_taxonomy_profiling'

    @classmethod
    def result_model(cls):
        """Return Kraken module's model class."""
        return KrakenResult

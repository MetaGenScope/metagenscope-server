"""Nanopore Taxa tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class NanoporeTaxaResult(ToolResult):
    """Nanopore tool's taxa result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


class NanoporeTaxaResultModule(ToolResultModule):
    """Nanopore Taxa tool module."""

    @classmethod
    def name(cls):
        """Return Nanopore Taxa module's unique identifier string."""
        return 'nanopore_taxa'

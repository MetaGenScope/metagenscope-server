"""
Reads Classified Module.

This chart shows the proportion of reads in each sample assigned to different groups.
"""

from app.display_modules.display_module import DisplayModule

# Re-export modules
from app.display_modules.reads_classified.reads_classified_models import (
    ReadsClassifiedResult,
    ReadsClassifiedDatum,
)
from app.display_modules.reads_classified.reads_classified_wrangler import ReadsClassifiedWrangler


class ReadsClassifiedModule(DisplayModule):
    """Reads Classified display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return []

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return 'reads_classified'

    @classmethod
    def get_result_model(cls):
        """Return data model for Reads Classified type."""
        return ReadsClassifiedResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Reads Classified type."""
        return ReadsClassifiedWrangler
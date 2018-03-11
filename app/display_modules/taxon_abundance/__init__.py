"""
Taxon Abundance module.

This plot shows the relative abundance of each different microbes found in
each sample.

Hover over the plot to highlight connections. Thicker connections represent
larger proportions of taxa in a given sample.
"""

from app.display_modules.display_module import DisplayModule

from app.display_modules.taxon_abundance.taxon_abundance_models import (
    TaxonAbundanceResult,
    TaxonAbundanceNode,
    TaxonAbundanceEdge,
)
from app.display_modules.taxon_abundance.taxon_abundance_wrangler import TaxonAbundanceWrangler


class TaxonAbundanceDisplayModule(DisplayModule):
    """Taxon Abundance display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return []

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return 'taxon_abundance'

    @classmethod
    def get_result_model(cls):
        """Return status wrapper for Taxon Abundance type."""
        return TaxonAbundanceResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Taxon Abundance type."""
        return TaxonAbundanceWrangler

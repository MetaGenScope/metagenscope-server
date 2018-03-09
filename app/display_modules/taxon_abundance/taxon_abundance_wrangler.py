"""Task for generating Taxon Abundance results."""

from app.display_modules.display_wrangler import DisplayModuleWrangler


class TaxonAbundanceWrangler(DisplayModuleWrangler):  # pylint: disable=abstract-method
    """Task for generating Taxon Abundance results."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return []

    @staticmethod
    def run_group(sample_group_id):
        """Gather samples and process."""
        return {'task': 'taxon_abundance'}

"""Task for generating Taxon Abundance results."""

from app.display_modules.display_task import DisplayModuleTask
from app.extensions import celery


class TaxonAbundanceTask(DisplayModuleTask):  # pylint: disable=abstract-method
    """Task for generating Taxon Abundance results."""

    @classmethod
    def required_tool_results(cls):
        """Enumerate which ToolResult modules a sample must have."""
        return []

    def run_group(self, sample_group_id):
        """Gather samples and process."""
        return {'task': 'taxon_abundance'}


TaxonAbundanceTask = celery.register_task(TaxonAbundanceTask())  # pylint: disable=invalid-name

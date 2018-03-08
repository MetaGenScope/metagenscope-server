"""Tasks for generating Reads Classified results."""

from app.display_modules.display_task import DisplayModuleTask
from app.extensions import celery


class ReadsClassifiedTask(DisplayModuleTask):  # pylint: disable=abstract-method
    """Task for generating Reads Classified results."""

    @classmethod
    def required_tool_results(cls):
        """Enumerate which ToolResult modules a sample must have."""
        return []

    def run_group(self, sample_group_id):
        """Gather group of samples and process."""
        return {'task': 'reads_classified'}


ReadsClassifiedTask = celery.register_task(ReadsClassifiedTask())  # pylint: disable=invalid-name

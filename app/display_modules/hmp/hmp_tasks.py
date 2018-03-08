"""Tasks for generating HMP results."""

from app.display_modules.display_task import DisplayModuleTask
from app.extensions import celery


class HMPTask(DisplayModuleTask):  # pylint: disable=abstract-method
    """Task for generating HMP results."""

    @classmethod
    def required_tool_results(cls):
        """Enumerate which ToolResult modules a sample must have."""
        return []

    def run_group(self, sample_group_id):
        """Gather group of samples and process."""
        return {'task': 'hmp'}


HMPTask = celery.register_task(HMPTask())  # pylint: disable=invalid-name

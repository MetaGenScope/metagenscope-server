"""Tasks for generating Sample Similarity results."""

from app.display_modules.display_task import DisplayModuleTask
from app.extensions import celery


class SampleSimilarityTask(DisplayModuleTask):  # pylint: disable=abstract-method
    """Task for generating Reads Classified results."""

    @classmethod
    def required_tool_results(cls):
        """Enumerate which ToolResult modules a sample must have."""
        return []

    def run_group(self, sample_group_id):
        """Gather samples and process."""
        return {'task': 'sample_similarity'}


SampleSimilarityTask = celery.register_task(SampleSimilarityTask())  # pylint: disable=invalid-name

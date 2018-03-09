"""Tasks for generating Reads Classified results."""

from app.display_modules.display_wrangler import DisplayModuleWrangler


class ReadsClassifiedWrangler(DisplayModuleWrangler):  # pylint: disable=abstract-method
    """Task for generating Reads Classified results."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return []

    @staticmethod
    def run_group(sample_group_id):
        """Gather group of samples and process."""
        return {'task': 'reads_classified'}

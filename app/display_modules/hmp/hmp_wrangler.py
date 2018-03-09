"""Tasks for generating HMP results."""

from app.display_modules.display_wrangler import DisplayModuleWrangler


class HMPWrangler(DisplayModuleWrangler):  # pylint: disable=abstract-method
    """Task for generating HMP results."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return []

    @staticmethod
    def run_group(sample_group_id):
        """Gather group of samples and process."""
        return {'task': 'hmp'}

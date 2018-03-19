"""Sample Similarity display module."""

from app.tool_results.read_stats import ReadStatsResultModule
from app.display_modules.display_module import DisplayModule

from .wrangler import ReadStatsResult, ReadStatsWrangler, MODULE_NAME


class ReadStatsDisplayModule(DisplayModule):
    """Read Stats display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [ReadStatsResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return ReadStatsResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return ReadStatsWrangler

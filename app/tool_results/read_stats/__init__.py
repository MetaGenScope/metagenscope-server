"""Read Stats tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class ReadStatsResult(ToolResult):     # pylint: disable=too-few-public-methods
    """Read Stats result type."""

    # Accept any JSON
    microbial = mongoDB.DynamicField(required=True)
    raw = mongoDB.DynamicField(required=True)


class ReadStatsResultModule(ToolResultModule):
    """Read Stats tool module."""

    @classmethod
    def name(cls):
        """Return Read Stats module's unique identifier string."""
        return 'read_stats'

    @classmethod
    def result_model(cls):
        """Return Read Stats module's model class."""
        return ReadStatsResult

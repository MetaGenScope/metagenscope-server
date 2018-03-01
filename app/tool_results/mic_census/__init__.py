"""Microbe Census tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class MicCensusResult(ToolResult):      # pylint: disable=too-few-public-methods
    """Mic Census tool's result type."""

    average_genome_size = mongoDB.IntField()
    total_bases = mongoDB.IntField()
    genome_equivalents = mongoDB.IntField()


class MicCensusResultModule(ToolResultModule):
    """Microbe Census tool module."""

    @classmethod
    def name(cls):
        """Return Microbe Census module's unique identifier string."""
        return 'mic_census'

    @classmethod
    def result_model(cls):
        """Return Microbe Census module's model class."""
        return MicCensusResult

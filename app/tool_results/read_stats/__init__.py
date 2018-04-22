"""Read Stats tool module."""

from app.extensions import mongoDB
from app.tool_results.modules import SampleToolResultModule
from app.tool_results.models import ToolResult


class ReadStatsToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """A set of consistent fields for read stats."""

    num_reads = mongoDB.IntField()
    gc_content = mongoDB.FloatField()
    codons = mongoDB.MapField(field=mongoDB.IntField(), required=True)
    tetramers = mongoDB.MapField(field=mongoDB.IntField(), required=True)

    @staticmethod
    def stat_fields():
        """Return a list of the stats collected."""
        return ['num_reads', 'gc_content', 'codons', 'tetramers']


class ReadStatsToolResultModule(SampleToolResultModule):
    """Read Stats tool module."""

    @classmethod
    def name(cls):
        """Return Read Stats module's unique identifier string."""
        return 'read_stats'

    @classmethod
    def result_model(cls):
        """Return Read Stats module's model class."""
        return ReadStatsToolResult

"""Microbe Census tool module."""
from mongoengine import ValidationError

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class MicCensusResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Mic Census tool's result type."""

    average_genome_size = mongoDB.IntField()
    total_bases = mongoDB.IntField()
    genome_equivalents = mongoDB.IntField()

    def clean(self):
        """Check all values are non-negative, if not raise an error."""
        def validate(*vals):
            """Check vals are non-negative, return a bool."""
            for val in vals:
                if val < 0:
                    return False
            return True

        if not validate(self.average_genome_size,
                        self.total_bases,
                        self.genome_equivalents):
            msg = f'MicCensusResult values must be non-negative'
            raise ValidationError(msg)


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

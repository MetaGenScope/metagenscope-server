"""Reads Classified tool module."""
from mongoengine import ValidationError

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class ReadsClassifiedResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Reads Classified tool's result type."""

    viral = mongoDB.IntField()
    archaea = mongoDB.IntField()
    bacteria = mongoDB.IntField()
    host = mongoDB.IntField()
    unknown = mongoDB.IntField()

    def clean(self):
        tot = sum([self.viral, self.archaea,
                   self.bacteria, self.host, self.unknown])
        tot = abs(tot - 1)
        if tot > 0.0001:
            msg = f'ReadsClassifiedResult fields do not sum to 1'
            raise ValidationError(msg)


class ReadsClassifiedResultModule(ToolResultModule):
    """Reads Classified tool module."""

    @classmethod
    def name(cls):
        """Return Reads Classified module's unique identifier string."""
        return 'reads_classified'

    @classmethod
    def result_model(cls):
        """Return Reads Classified module's model class."""
        return ReadsClassifiedResult

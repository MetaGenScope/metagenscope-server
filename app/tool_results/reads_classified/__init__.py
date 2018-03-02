"""Reads Classified tool module."""
from math import isclose
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
        """Checl that the sum is near 1."""
        tot = sum([self.viral, self.archaea,
                   self.bacteria, self.host, self.unknown])
        if not isclose(tot, 1.0):
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

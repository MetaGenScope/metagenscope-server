"""Reads Classified tool module."""
from math import isclose
from mongoengine import ValidationError

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class ReadsClassifiedResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Reads Classified tool's result type."""

    viral = mongoDB.IntField(required=True, default=0)
    archaea = mongoDB.IntField(required=True, default=0)
    bacteria = mongoDB.IntField(required=True, default=0)
    host = mongoDB.IntField(required=True, default=0)
    unknown = mongoDB.IntField(required=True, default=0)


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

    @classmethod
    def make_result_model(cls, post_json):
        """Spread JSON values before creating result model."""
        return cls.result_model()(**post_json)

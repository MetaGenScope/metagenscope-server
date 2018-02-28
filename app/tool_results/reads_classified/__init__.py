"""Reads Classified tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class ReadsClassifiedResult(ToolResult):
    """Reads Classified tool's result type."""

    viral = mongoDB.IntField()
    archaea = mongoDB.IntField()
    bacteria = mongoDB.IntField()
    host = mongoDB.IntField()
    unknown = mongoDB.IntField()


class ReadsClassifiedResultModule(ToolResultModule):
    """Reads Classified tool module."""

    @classmethod
    def name(cls):
        """Return Reads Classified module's unique identifier string."""
        return 'reads_classified'

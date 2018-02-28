"""Reads Classified tool module."""

from app.extensions import mongoDB
from app.tool_modules.tool_module import ToolModule


class ReadsClassifiedResult(ToolModule):
    """Reads Classified tool's result type."""

    viral = mongoDB.IntField()
    archaea = mongoDB.IntField()
    bacteria = mongoDB.IntField()
    host = mongoDB.IntField()
    unknown = mongoDB.IntField()

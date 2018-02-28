"""Metaphlan 2 tool module."""

from app.extensions import mongoDB
from app.tool_modules.tool_module import ToolModule


class Metaphlan2Result(ToolModule):
    """Metaphlan 2 tool's result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()

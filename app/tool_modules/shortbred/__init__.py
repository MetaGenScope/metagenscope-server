"""Shortbred tool module."""

from app.extensions import mongoDB
from app.tool_modules.tool_module import ToolModule


class ShortbredResult(ToolModule):
    """Shortbred tool's result type."""

    abundances = mongoDB.DictField()

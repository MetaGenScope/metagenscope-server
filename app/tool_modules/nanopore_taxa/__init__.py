"""Nanopore Taxa tool module."""

from app.extensions import mongoDB
from app.tool_modules.tool_module import ToolModule


class NanoporeTaxaResult(ToolModule):
    """Nanopore tool's taxa result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()

"""Models for Macrobial tool module."""

from app.extensions import mongoDB
from app.tool_results.models import ToolResult


class MacrobialRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in Macrobial."""

    total_reads = mongoDB.IntField()
    rpkm = mongoDB.FloatField()


class MacrobeToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Macrobial result type."""

    macrobe_row_field = mongoDB.EmbeddedDocumentField(MacrobialRow)
    macrobes = mongoDB.MapField(field=macrobe_row_field, required=True)

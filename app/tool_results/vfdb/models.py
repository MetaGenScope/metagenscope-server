"""Models for Virulence Factor tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult


class VFDBRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in VFDB."""

    rpk = mongoDB.FloatField()
    rpkm = mongoDB.FloatField()
    rpkmg = mongoDB.FloatField()


class VFDBToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Virulence Factor result type."""

    vfdb_row_field = mongoDB.EmbeddedDocumentField(VFDBRow)
    genes = mongoDB.MapField(field=vfdb_row_field, required=True)

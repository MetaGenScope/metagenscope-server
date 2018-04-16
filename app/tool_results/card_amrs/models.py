"""Models for Virulence Factor tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult


class AMRRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in CARD AMR Alignment."""

    rpk = mongoDB.FloatField()
    rpkm = mongoDB.FloatField()
    rpkmg = mongoDB.FloatField()


class CARDAMRToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """CARD AMR Alignment result type."""

    amr_row_field = mongoDB.EmbeddedDocumentField(AMRRow)
    genes = mongoDB.MapField(field=amr_row_field, required=True)

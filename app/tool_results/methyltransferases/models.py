"""Models for Methyltransferase tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult


class MethylRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in Methyltransferase."""

    rpk = mongoDB.FloatField()
    rpkm = mongoDB.FloatField()
    rpkmg = mongoDB.FloatField()


class MethylToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Methyltransferase result type."""

    row_field = mongoDB.EmbeddedDocumentField(MethylRow)
    genes = mongoDB.MapField(field=row_field, required=True)

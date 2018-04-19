"""Models for Methyltransferase tool module."""

from app.extensions import mongoDB
from app.tool_results.models import ToolResult


class MethylRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in Methyltransferase."""

    rpk = mongoDB.FloatField()
    rpkm = mongoDB.FloatField()
    rpkmg = mongoDB.FloatField()


class MethylToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Methyltransferase result type."""

    genes = mongoDB.MapField(field=mongoDB.EmbeddedDocumentField(MethylRow),
                             required=True)

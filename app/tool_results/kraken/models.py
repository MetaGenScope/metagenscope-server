"""Models for Kraken tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult


class KrakenResult(ToolResult):     # pylint: disable=too-few-public-methods
    """Kraken tool's result type."""

    # Taxa is of the form: {<taxon_name>: <abundance_value>}
    taxa = mongoDB.MapField(mongoDB.IntField(), required=True)

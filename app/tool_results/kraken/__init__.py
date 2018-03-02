"""Kraken tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class KrakenResult(ToolResult):     # pylint: disable=too-few-public-methods
    """Kraken tool's result type."""

    # Taxa is of the form: {<taxon_name>: <abundance_value>}
    taxa = mongoDB.DictField()


class KrakenResultModule(ToolResultModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return 'kraken'

    @classmethod
    def result_model(cls):
        """Return Kraken module's model class."""
        return KrakenResult

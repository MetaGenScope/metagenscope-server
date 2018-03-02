"""Metaphlan 2 tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class Metaphlan2Result(ToolResult):     # pylint: disable=too-few-public-methods
    """Metaphlan 2 tool's result type."""

    # Taxa is of the form: {<taxon_name>: <abundance_value>}
    taxa = mongoDB.MapField(mongoDB.IntField(), required=True)


class Metaphlan2ResultModule(ToolResultModule):
    """Metaphlan 2 tool module."""

    @classmethod
    def name(cls):
        """Return Metaphlan 2 module's unique identifier string."""
        return 'metaphlan2'

    @classmethod
    def result_model(cls):
        """Return Metaphlan2 module's model class."""
        return Metaphlan2Result

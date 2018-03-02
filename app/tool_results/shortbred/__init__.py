"""Shortbred tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class ShortbredResult(ToolResult):      # pylint: disable=too-few-public-methods
    """Shortbred tool's result type."""

    # Abundances is of the form: {<amr_gene>: <abundance_value>}
    abundances = mongoDB.DictField()


class ShortbredResultModule(ToolResultModule):
    """Shortbred tool module."""

    @classmethod
    def name(cls):
        """Return Shortbred module's unique identifier string."""
        return 'shortbred'

    @classmethod
    def result_model(cls):
        """Return Shortbred module's model class."""
        return ShortbredResult

    @classmethod
    def make_result_model(cls, post_json):
        """Process uploaded JSON (if necessary) and create result model."""
        return cls.result_model()(post_json)

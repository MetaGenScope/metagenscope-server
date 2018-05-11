"""Shortbred tool module."""

from app.extensions import mongoDB
from app.tool_results.modules import SampleToolResultModule
from app.tool_results.models import ToolResult


class ShortbredResult(ToolResult):      # pylint: disable=too-few-public-methods
    """Shortbred tool's result type."""

    # Abundances is of the form: {<amr_gene>: <abundance_value>}
    abundances = mongoDB.MapField(mongoDB.FloatField(), required=True)


class ShortbredResultModule(SampleToolResultModule):
    """Shortbred tool module."""

    @classmethod
    def name(cls):
        """Return Shortbred module's unique identifier string."""
        return 'shortbred_amr_profiling'

    @classmethod
    def result_model(cls):
        """Return Shortbred module's model class."""
        return ShortbredResult

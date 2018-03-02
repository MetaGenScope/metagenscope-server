"""HMP Sites tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class HmpSitesResult(ToolResult):       # pylint: disable=too-few-public-methods
    """HMP Sites tool's result type."""

    gut = mongoDB.FloatField()
    skin = mongoDB.FloatField()
    throat = mongoDB.FloatField()
    urogenital = mongoDB.FloatField()
    airways = mongoDB.FloatField()


class HmpSitesResultModule(ToolResultModule):
    """HMP Sites tool module."""

    @classmethod
    def name(cls):
        """Return HMP Sites module's unique identifier string."""
        return 'hmp_sites'

    @classmethod
    def result_model(cls):
        """Return HMP Sites module's model class."""
        return HmpSitesResult

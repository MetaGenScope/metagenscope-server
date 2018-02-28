"""HMP Sites tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class HmpSitesResult(ToolResult):
    """HMP Sites tool's result type."""

    gut = mongoDB.IntField()
    skin = mongoDB.IntField()
    throat = mongoDB.IntField()


class HmpSitesResultModule(ToolResultModule):
    """HMP Sites tool module."""

    @classmethod
    def name(cls):
        """Return HMP Sites module's unique identifier string."""
        return 'hmp_sites'

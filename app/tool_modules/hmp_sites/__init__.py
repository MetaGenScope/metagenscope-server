"""HMP Sites tool module."""

from app.extensions import mongoDB
from app.tool_modules.tool_module import ToolModule


class HmpSitesResult(ToolModule):
    """HMP Sites tool's result type."""

    gut = mongoDB.IntField()
    skin = mongoDB.IntField()
    throat = mongoDB.IntField()

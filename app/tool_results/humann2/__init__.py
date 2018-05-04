"""HUMANn2 tool module."""

from app.extensions import mongoDB
from app.tool_results.modules import SampleToolResultModule
from app.tool_results.models import ToolResult

from .constants import MODULE_NAME


EmbeddedDoc = mongoDB.EmbeddedDocumentField  # pylint: disable=invalid-name


class Humann2PathwaysRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a pathways in humann2."""

    abundance = mongoDB.FloatField()
    coverage = mongoDB.FloatField()


class Humann2Result(ToolResult):  # pylint: disable=too-few-public-methods
    """HUMANn2 result type."""

    pathways = mongoDB.MapField(field=EmbeddedDoc(Humann2PathwaysRow), required=True)


class Humann2ResultModule(SampleToolResultModule):
    """HUMANn2 tool module."""

    @classmethod
    def name(cls):
        """Return HUMANn2 module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return HUMANn2 module's model class."""
        return Humann2Result

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, pathways."""
        return [lambda payload: {'pathways': payload}]

"""HUMANn2 tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


EmbeddedDoc = mongoDB.EmbeddedDocumentField  # pylint: disable=invalid-name


class Humann2PathwaysRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a pathways in humann2."""

    abundance = mongoDB.FloatField()
    coverage = mongoDB.FloatField()


class Humann2Result(ToolResult):  # pylint: disable=too-few-public-methods
    """HUMANn2 result type."""

    pathways = mongoDB.MapField(field=EmbeddedDoc(Humann2PathwaysRow), required=True)
    genes = mongoDB.MapField(field=mongoDB.FloatField(), required=True)


class Humann2ResultModule(ToolResultModule):
    """HUMANn2 tool module."""

    @classmethod
    def name(cls):
        """Return HUMANn2 module's unique identifier string."""
        return 'humann2_functional_profiling'

    @classmethod
    def result_model(cls):
        """Return HUMANn2 module's model class."""
        return Humann2Result

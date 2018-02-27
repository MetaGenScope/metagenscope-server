"""Sample Similarity display module."""

from mongoengine import ValidationError

from app.api.v1.display_modules.display_module import DisplayModule
from app.extensions import mongoDB as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class SampleSimilarityDisplayModule(DisplayModule):
    """Sample Similarity display module."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return 'sample_similarity'

    @classmethod
    def get_query_result_wrapper_field(cls):
        """Return status wrapper for Sample Similarity type."""
        return EmbeddedDoc(SampleSimilarityResult)

    @classmethod
    def get_mongodb_embedded_docs(cls):
        """Return sub-document types for Sample Similarity type."""
        return [
            ToolDocument,
            SampleSimilarityResult,
        ]


class ToolDocument(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Tool document type."""

    x_label = mdb.StringField(required=True)
    y_label = mdb.StringField(required=True)


class SampleSimilarityResult(mdb.EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Sample Similarity document type."""

    categories = mdb.MapField(field=StringList, required=True)
    tools = mdb.MapField(field=EmbeddedDoc(ToolDocument), required=True)
    data_records = mdb.ListField(mdb.DictField(), required=True)

    def clean(self):
        """Ensure that `data_records` contain valid records."""
        category_names = self.categories.keys()
        tool_names = self.tools.keys()

        for record in self.data_records:
            for category_name in category_names:
                if category_name not in record:
                    msg = 'Record must have all categories.'
                    raise ValidationError(msg)
            for tool_name in tool_names:
                xname = '{}_x'.format(tool_name)
                yname = '{}_y'.format(tool_name)
                if (xname not in record) or (yname not in record):
                    msg = 'Record must x and y for all tools.'
                    raise ValidationError(msg)

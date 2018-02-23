from .display_module import DisplayModule
from app.extensions import mongoDB as mdb
from mongoengine import ValidationError

EmDoc = mdb.EmbeddedDocumentField
StringList = mdb.ListField(mdb.StringField())


class SampleSimilarityDisplayModule(DisplayModule):

    @classmethod
    def name(ctype):
        return 'sample_similarity'

    @classmethod
    def get_data(ctype, my_result):
        return my_result

    @classmethod
    def get_query_result_wrapper_field(ctype):
        return EmDoc(SampleSimilarityResult)

    @classmethod
    def get_mongodb_embedded_docs(ctype):
        return [ToolDocument, SampleSimilarityResult]


class ToolDocument(mdb.EmbeddedDocument):
    """Tool document type."""

    x_label = mdb.StringField(required=True)
    y_label = mdb.StringField(required=True)


class SampleSimilarityResult(mdb.EmbeddedDocument):
    """Sample Similarity document type."""

    categories = mdb.MapField(field=StringList, required=True)
    tools = mdb.MapField(field=EmDoc(ToolDocument), required=True)
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

from .display_module import DisplayModule
from app.extensions import mongoDB
from mongoengine import ValidationError


class SampleSimilarityDisplayModule(DisplayModule):

    def name(self):
        return 'sample_similarity'

    def get_data(self, my_result):
        return my_result

    def get_query_result_wrapper_field(self):
        return mongoDB.EmbeddedDocumentField(SampleSimilarityResult)

    def get_mongodb_embedded_docs(self):
        return [SampleSimilarityResult]


class SampleSimilarityResult(mongoDB.EmbeddedDocument):
    """Sample Similarity document type."""

    categories = mongoDB.MapField(field=mongoDB.ListField(mongoDB.StringField()), required=True)
    tools = mongoDB.MapField(field=mongoDB.EmbeddedDocumentField(ToolDocument), required=True)
    data_records = mongoDB.ListField(mongoDB.DictField(), required=True)

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

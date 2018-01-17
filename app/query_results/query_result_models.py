"""Query Result model definitions."""

import datetime

from mongoengine import ValidationError

from app.extensions import mongoDB


# pylint: disable=too-few-public-methods
class ToolDocument(mongoDB.EmbeddedDocument):
    """Tool document type."""

    x_label = mongoDB.StringField(required=True)
    y_label = mongoDB.StringField(required=True)


# pylint: disable=too-few-public-methods
class SampleSimilarityResult(mongoDB.EmbeddedDocument):
    """Sample Similarity document type."""

    categories = mongoDB.MapField(field=mongoDB.ListField(mongoDB.StringField()))
    tools = mongoDB.MapField(field=mongoDB.EmbeddedDocumentField(ToolDocument))
    data_records = mongoDB.ListField(mongoDB.DictField())

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
                if '%s_x' % tool_name not in record or '%s_y' % tool_name not in record:
                    msg = 'Record must x and y for all tools.'
                    raise ValidationError(msg)


QUERY_RESULT_STATUS = (('E', 'ERROR'),
                       ('P', 'PENDING'),
                       ('W', 'WORKING'),
                       ('S', 'SUCCESS'))


class QueryResult(mongoDB.Document):
    """Base mongo result class."""

    status = mongoDB.StringField(required=True,
                                 max_length=1,
                                 choices=QUERY_RESULT_STATUS,
                                 default='P')
    sample_group_id = mongoDB.UUIDField(binary=False)
    sample_similarity = mongoDB.EmbeddedDocumentField(SampleSimilarityResult)
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'indexes': ['sample_group_id']
    }

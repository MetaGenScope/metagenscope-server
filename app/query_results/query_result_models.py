"""Query Result model definitions."""

import datetime
from app.extensions import mongoDB


QUERY_RESULT_STATUS = (('E', 'ERROR'),
                       ('P', 'PENDING'),
                       ('W', 'WORKING'),
                       ('S', 'SUCCESS'))


class QueryResultWrapper(mongoDB.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Base mongo result class."""

    status = mongoDB.StringField(required=True,
                                 max_length=1,
                                 choices=QUERY_RESULT_STATUS,
                                 default='P')

    meta = {'allow_inheritance': True}


class QueryResultMeta(mongoDB.DynamicDocument):
    """Base mongo result class."""

    sample_group_id = mongoDB.UUIDField(binary=False)
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)
    meta = {
        'indexes': ['sample_group_id']
    }

    @property
    def result_types(self):
        """Return a list of all query result types available for this record."""
        blacklist = ['id', 'sample_group_id', 'created_at']
        all_fields = [k
                      for k, v in self.__class__._fields.items()  # pylint: disable=no-member
                      if k not in blacklist]
        return [field for field in all_fields if hasattr(self, field)]

    @classmethod
    def build_result_type(cls, name):
        """Build result type for query result model."""
        out = type(name, (cls,), {})
        return out

    @classmethod
    def add_property(cls, name, obj):
        """Expose wrapper for setting attribute."""
        setattr(cls, name, property(obj))

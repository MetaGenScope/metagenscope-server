"""Analysis Results model definitions."""

import datetime
from uuid import uuid4

from app.extensions import mongoDB


ANALYSIS_RESULT_STATUS = (('E', 'ERROR'),
                          ('P', 'PENDING'),
                          ('W', 'WORKING'),
                          ('S', 'SUCCESS'))


class AnalysisResultWrapper(mongoDB.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Base mongo result class."""

    status = mongoDB.StringField(required=True,
                                 max_length=1,
                                 choices=ANALYSIS_RESULT_STATUS,
                                 default='P')

    meta = {'allow_inheritance': True}


class AnalysisResultMeta(mongoDB.DynamicDocument):
    """Base mongo result class."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False, default=uuid4)
    sample_group_id = mongoDB.UUIDField(binary=False)
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'indexes': ['sample_group_id']
    }

    @property
    def result_types(self):
        """Return a list of all analysis result types available for this record."""
        blacklist = ['uuid', 'sample_group_id', 'created_at']
        all_fields = [k
                      for k, v in vars(self).items()  # pylint: disable=no-member
                      if k not in blacklist and not k.startswith('_')]
        return [field for field in all_fields if hasattr(self, field)]

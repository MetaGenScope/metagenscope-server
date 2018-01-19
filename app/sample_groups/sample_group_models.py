"""Sample Group model definitions."""

import datetime

from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields
from mongoengine import DoesNotExist

from app.extensions import db
from app.query_results.query_result_models import QueryResult


# pylint: disable=too-few-public-methods
class SampleGroup(db.Model):
    """MetaGenScope Sample Group model."""

    __tablename__ = 'sample_groups'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))
    name = db.Column(db.String(128), unique=True, nullable=False)
    access_scheme = db.Column(db.String(128), default='public', nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(
            self, name, access_scheme='public',
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        self.name = name
        self.access_scheme = access_scheme
        self.created_at = created_at

    def query_result(self):
        """Get sample group's query result model."""
        try:
            return QueryResult.objects.get(sample_group_id=self.id)
        except DoesNotExist:
            return None


class SampleGroupSchema(Schema):
    """Serializer for Sample Group."""

    id = fields.Str()
    name = fields.Str()
    access_scheme = fields.Str()
    created_at = fields.Date()


sample_group_schema = SampleGroupSchema()   # pylint: disable=invalid-name

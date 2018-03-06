"""Sample Group model definitions."""

import datetime

from sqlalchemy.dialects.postgresql import UUID
from marshmallow import fields
from mongoengine import DoesNotExist

from app.base import BaseSchema
from app.extensions import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta


# pylint: disable=too-few-public-methods
class SampleGroup(db.Model):
    """MetaGenScope Sample Group model."""

    __tablename__ = 'sample_groups'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))

    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id'))

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

    @property
    def analysis_result(self):
        """Get sample group's analysis result model."""
        try:
            return AnalysisResultMeta.objects.get(sample_group_id=self.id)
        except DoesNotExist:
            return None


class SampleGroupSchema(BaseSchema):
    """Serializer for Sample Group."""

    __envelope__ = {
        'single': 'sample_group',
        'many': 'sample_groups',
    }
    __model__ = SampleGroup

    uuid = fields.Str()
    name = fields.Str()
    access_scheme = fields.Str()
    created_at = fields.Date()


sample_group_schema = SampleGroupSchema()   # pylint: disable=invalid-name

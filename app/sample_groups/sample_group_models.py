"""Sample Group model definitions."""

import datetime

from marshmallow import fields
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.base import BaseSchema
from app.extensions import db
from app.samples.sample_models import Sample


class SamplePlaceholder(db.Model):  # pylint: disable=too-few-public-methods
    """Placeholder for Mongo Sample in SampleGroup<->Sample relationship."""

    sample_id = db.Column(UUID(as_uuid=True), primary_key=True)
    sample_group_id = db.Column(UUID(as_uuid=True),
                                db.ForeignKey('sample_groups.id'),
                                primary_key=True)

    def __init__(self, sample_id=None, sample_group_id=None):
        """Initialize SampleGroup<->SamplePlaceholder model."""
        self.sample_id = sample_id
        self.sample_group_id = sample_group_id


class SampleGroup(db.Model):
    """MetaGenScope Sample Group model."""

    __tablename__ = 'sample_groups'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))

    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organizations.id'))

    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=False, default='')
    access_scheme = db.Column(db.String(128), default='public', nullable=False)
    theme = db.Column(db.String(16), nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False)

    sample_placeholders = db.relationship(SamplePlaceholder)
    sample_ids = association_proxy('sample_placeholders', 'sample_id')

    analysis_result_uuid = db.Column(UUID(as_uuid=True), nullable=False)

    def __init__(  # pylint: disable=too-many-arguments
            self, name, analysis_result, description='',
            access_scheme='public', theme='',
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        self.name = name
        self.description = description
        self.access_scheme = access_scheme
        self.theme = theme
        self.created_at = created_at
        self.analysis_result_uuid = analysis_result.uuid

    @property
    def samples(self):
        """
        Get SampleGroup's associated Samples.

        This will hit Mongo every time it is called! Responsibility for caching
        the result lies on the calling method.
        """
        return Sample.objects(uuid__in=self.sample_ids)

    @samples.setter
    def samples(self, value):
        """Set SampleGroup's samples."""
        self.sample_ids = [sample.uuid for sample in value]

    @samples.deleter
    def samples(self):
        """Remove SampleGroup's samples."""
        self.sample_ids = []

    @property
    def tools_present(self):
        """Return list of names for Tool Results present across all Samples in this group."""
        # Cache samples
        samples = self.samples

        tools_present_in_all = set([])
        for i, sample in enumerate(samples):
            tool_results = set(sample.tool_result_names)
            if i == 0:
                tools_present_in_all |= tool_results
            else:
                tools_present_in_all &= tool_results
        return list(tools_present_in_all)

    @property
    def analysis_result(self):
        """Get sample group's analysis result model."""
        return AnalysisResultMeta.objects.get(uuid=self.analysis_result_uuid)

    @analysis_result.setter
    def analysis_result(self, new_analysis_result):
        """Store new analysis result UUID (caller must still commit session!)."""
        self.analysis_result_uuid = new_analysis_result.uuid


class SampleGroupSchema(BaseSchema):  # pylint: disable=too-few-public-methods
    """Serializer for Sample Group."""

    __envelope__ = {
        'single': 'sample_group',
        'many': 'sample_groups',
    }
    __model__ = SampleGroup

    uuid = fields.Str()
    name = fields.Str()
    description = fields.Str()
    access_scheme = fields.Str()
    theme = fields.Str()
    created_at = fields.Date()
    analysis_result_uuid = fields.Str()


sample_group_schema = SampleGroupSchema()   # pylint: disable=invalid-name

"""Sample Group model definitions."""

import datetime

from marshmallow import fields, pre_dump
from mongoengine import DoesNotExist
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
    access_scheme = db.Column(db.String(128), default='public', nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    sample_placeholders = db.relationship(SamplePlaceholder)
    sample_ids = association_proxy('sample_placeholders', 'sample_id')

    def __init__(
            self, name, access_scheme='public',
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        self.name = name
        self.access_scheme = access_scheme
        self.created_at = created_at

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
        try:
            return AnalysisResultMeta.objects.get(sample_group_id=self.id)
        except DoesNotExist:
            return None


class SampleGroupSchema(BaseSchema):  # pylint: disable=too-few-public-methods
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

    @pre_dump(pass_many=False)
    # pylint: disable=no-self-use
    def add_analysis_result(self, sample_group):
        """Add analysis result's ID, if it exists."""
        analysis_result = sample_group.analysis_result
        if analysis_result:
            sample_group.analysis_result_id = str(analysis_result.id)
        return sample_group


sample_group_schema = SampleGroupSchema()   # pylint: disable=invalid-name

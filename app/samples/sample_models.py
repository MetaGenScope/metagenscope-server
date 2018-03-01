"""Sample model definitions."""

import datetime

from uuid import uuid4

from marshmallow import fields

from app.base import BaseSchema
from app.extensions import mongoDB
from app.tool_results import all_tool_result_modules


class BaseSample(mongoDB.Document):
    """Sample model."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False, default=uuid4)
    name = mongoDB.StringField(unique=True)
    metadata = mongoDB.DictField(default={})
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'allow_inheritance': True}


# Create actual Sample class based on modules present at runtime
Sample = type('Sample', (BaseSample,), {
    module.name(): mongoDB.EmbeddedDocumentField(module.result_model())
    for module in all_tool_result_modules})


class SampleSchema(BaseSchema):
    """Serializer for Sample."""

    __envelope__ = {
        'single': 'sample',
        'many': 'samples',
    }
    __model__ = Sample

    uuid = fields.Str()
    name = fields.Str()
    metadata = fields.Dict()
    created_at = fields.Date()


sample_schema = SampleSchema()   # pylint: disable=invalid-name

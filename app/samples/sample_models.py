"""Sample model definitions."""

import datetime

from uuid import uuid4

from app.extensions import mongoDB


class Sample(mongoDB.Document):
    """Sample model."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False, default=uuid4)
    name = mongoDB.StringField(unique=True)
    metadata = mongoDB.DictField(default={})
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

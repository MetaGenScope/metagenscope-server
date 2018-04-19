"""Reads Classified display models."""

from app.extensions import mongoDB as mdb


class SingleReadsClassifiedResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Reads Classified for one sample"""

    viral = mdb.IntField(required=True, default=0)
    archaea = mdb.IntField(required=True, default=0)
    bacteria = mdb.IntField(required=True, default=0)
    host = mdb.IntField(required=True, default=0)
    unknown = mdb.IntField(required=True, default=0)


class ReadsClassifiedResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    samples = mdb.MapField(field=SingleReadsClassifiedResult, required=True)

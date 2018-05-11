"""Microbe Directory display models."""

from app.extensions import mongoDB as mdb


class MicrobeDirectoryResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Set of microbe directory results."""

    samples = mdb.DictField(required=True)

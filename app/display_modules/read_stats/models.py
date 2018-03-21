"""Read Stats display models."""

from app.extensions import mongoDB as mdb


class ReadStatsResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    samples = mdb.MapField(field=mdb.DynamicField(), required=True)

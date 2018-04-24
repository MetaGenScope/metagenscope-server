"""Macrobe display models."""

from app.extensions import mongoDB as mdb


class MacrobeResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Set of macrobe results."""

    samples = mdb.MapField(mdb.FloatField(), required=True)

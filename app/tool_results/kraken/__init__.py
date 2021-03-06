"""Kraken tool module."""

from app.tool_results.modules import SampleToolResultModule

from .constants import MODULE_NAME
from .models import KrakenResult


class KrakenResultModule(SampleToolResultModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Kraken module's model class."""
        return KrakenResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'taxa': payload}]

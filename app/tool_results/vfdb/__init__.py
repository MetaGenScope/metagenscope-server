"""Virulence Factor tool module."""

from app.tool_results.modules import SampleToolResultModule

from .models import VFDBToolResult


class VFDBResultModule(SampleToolResultModule):
    """Virulence Factor tool module."""

    @classmethod
    def name(cls):
        """Return Virulence Factor module's unique identifier string."""
        return 'vfdb_quantify'

    @classmethod
    def result_model(cls):
        """Return Virulence Factor module's model class."""
        return VFDBToolResult

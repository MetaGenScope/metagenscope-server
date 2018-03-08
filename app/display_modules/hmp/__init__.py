"""
HMP Module.

This chart shows the average similarity between bacterial communities in the
samples and human body sites from the Human Microbiome Project.
"""

from app.display_modules.display_module import DisplayModule
from app.display_modules.hmp.hmp_models import HMPResult
from app.display_modules.hmp.hmp_tasks import HMPTask


class HMPModule(DisplayModule):
    """HMP display module."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return 'hmp'

    @classmethod
    def get_result_model(cls):
        """Return data model for HMP type."""
        return HMPResult

    @classmethod
    def get_result_task(cls):
        """Return middleware task for HMP type."""
        return HMPTask

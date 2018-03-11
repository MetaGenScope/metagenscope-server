"""
Sample Similarity module.

This plot displays a dimensionality reduction of the data.

Samples are drawn near to similar samples in high dimensional space using a
machine learning algorithm: T-Stochastic Neighbours Embedding.

The plot can be colored by different sample metadata and the position of the
points can be adjust to reflect the analyses of different tools.
"""

from app.display_modules.display_module import DisplayModule
from app.display_modules.sample_similarity.constants import MODULE_NAME

# Re-export modules
from app.display_modules.sample_similarity.sample_similarity_models import (
    SampleSimilarityResult,
    ToolDocument,
)
from app.display_modules.sample_similarity.sample_similarity_wrangler import (
    SampleSimilarityWrangler,
)
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule


class SampleSimilarityDisplayModule(DisplayModule):
    """Sample Similarity display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [KrakenResultModule, Metaphlan2ResultModule]

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return data model for Sample Similarity type."""
        return SampleSimilarityResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Sample Similarity type."""
        return SampleSimilarityWrangler

"""Factory for generating Metaphlan2 result models for testing."""

from app.tool_results.kraken.tests.factory import create_values
from app.tool_results.metaphlan2 import Metaphlan2Result


def create_metaphlan2(taxa_count=10):
    """Create Metaphlan2Result with specified number of taxa."""
    taxa = create_values(taxa_count=taxa_count)
    return Metaphlan2Result(taxa=taxa).save()

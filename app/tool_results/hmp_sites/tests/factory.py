"""Factory for generating HMP tool result models for testing."""

from random import random

from app.tool_results.hmp_sites import HmpSitesResult


def create_values():
    """Create plausible data for hmp sites."""
    return {
        'skin': random(),
        'oral': random(),
        'urogenital': random(),
        'airways': random(),
    }


def create_hmp_sites():
    """Create HmpSitesResult with randomized fields."""
    packed_data = create_values()
    return HmpSitesResult(**packed_data)

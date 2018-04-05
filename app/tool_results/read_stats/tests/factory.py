"""Factory for generating Read Stat result models for testing."""

from random import randint, random

from app.tool_results.read_stats import ReadStatsToolResult


def create_tetramers():
    """Return a dict with plausible values for tetramers.

    N.B. this is broken in the CAP, this test reflects the broken state.
    """
    return {'C': randint(100, 1000),
            'T': randint(100, 1000),
            'A': randint(100, 1000),
            'G': randint(100, 1000)}


def create_codons():
    """Return a dict with plausible values for codons.

    N.B. this is broken in the CAP, this test reflects the broken state.
    """
    return {'C': randint(100, 1000),
            'T': randint(100, 1000),
            'A': randint(100, 1000),
            'G': randint(100, 1000)}


def create_one():
    """Return a dict for one read stats section."""
    return {
        'num_reads': randint(100 * 1000, 1000 * 1000),
        'gc_content': random(),
        'codons': create_codons(),
        'tetramers': create_tetramers()
    }


def create_values():
    """Create read stat values."""
    return {'raw': create_one(), 'microbial': create_one()}


def create_read_stats():
    """Create ReadStatsResult with randomized field data."""
    packed_data = create_values()
    return ReadStatsToolResult(**packed_data)

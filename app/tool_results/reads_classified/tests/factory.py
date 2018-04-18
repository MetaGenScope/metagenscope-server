"""Factory for generating Reads CLassified result models for testing."""

from random import randint

from app.tool_results.reads_classified import ReadsClassifiedResult


def create_values():
    """Create reads classified values."""
    return {
        'viral': randint(1000, 1000 * 1000),
        'archaea': randint(1000, 1000 * 1000),
        'bacteria': randint(1000, 1000 * 1000),
        'host': randint(1000, 1000 * 1000),
        'unknown': randint(1000, 1000 * 1000),
    }


def create_read_stats():
    """Create ReadStatsResult with randomized field data."""
    packed_data = create_values()
    return ReadsClassifiedToolResult(**packed_data)
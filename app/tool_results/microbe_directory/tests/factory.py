"""Factory for generating Kraken result models for testing."""

import random

from app.tool_results.microbe_directory import MicrobeDirectoryToolResult


def create_values():
    """Create microbe directory values."""
    result = {}
    for field in MicrobeDirectoryToolResult._fields:
        field_value = [['NaN', random.random()]]
        for i in range(random.randint(3, 6)):  # pylint: disable=unused-variable
            # Create random numeric key
            random_key = random.random() * 10
            key = f'{random_key:.2f}'
            field_value.append([key, random.random()])
        result[field] = field_value
    return result


def create_microbe_directory():
    """Create MicrobeDirectoryToolResult with randomized field data."""
    packed_data = create_values()
    return MicrobeDirectoryToolResult(**packed_data)

"""
DEPRECATED: Food and Pet tool module.

This module is different in the new pipeline and should be ignored for now.
"""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class FoodPetResult(ToolResult):        # pylint: disable=too-few-public-methods
    """Food/Pet tool's result type."""

    # DictFields are of the form: {<sample_id>: <sample_value>}
    vegetables = mongoDB.DictField(default={})
    fruits = mongoDB.DictField(default={})
    pets = mongoDB.DictField(default={})
    meats = mongoDB.DictField(default={})

    total_reads = mongoDB.IntField()


class FoodPetResultModule(ToolResultModule):
    """Food and Pet tool module."""

    @classmethod
    def name(cls):
        """Return Food and Pet module's unique identifier string."""
        return 'food_and_pet'

    @classmethod
    def result_model(cls):
        """Return Food and Pet module's model class."""
        return FoodPetResult

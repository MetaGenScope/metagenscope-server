"""Food and Pet tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class FoodPetResult(ToolResult):
    """Food/Pet tool's result type."""

    vegetables = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    fruits = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    pets = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    meats = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    total_reads = mongoDB.IntField()


class FoodPetResultModule(ToolResultModule):
    """Food and Pet tool module."""

    @classmethod
    def name(cls):
        """Return Food and Pet module's unique identifier string."""
        return 'food_and_pet'

"""Food and Pet tool module."""

from app.extensions import mongoDB
from app.tool_modules.tool_module import ToolModule


class FoodPetResult(ToolModule):
    """Food/Pet tool's result type."""

    vegetables = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    fruits = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    pets = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    meats = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    total_reads = mongoDB.IntField()

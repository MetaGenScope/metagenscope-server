"""Microbe Census tool module."""

from app.extensions import mongoDB
from app.tool_modules.tool_module import ToolModule


class MicCensusResult(ToolModule):
    """Mic Census tool's result type."""

    average_genome_size = mongoDB.IntField()
    total_bases = mongoDB.IntField()
    genome_equivalents = mongoDB.IntField()

"""Microbe Directory tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class MicrobeDirectoryResult(ToolResult):     # pylint: disable=too-few-public-methods
    """Microbe Directory result type."""

    # Accept any JSON
    antimicrobial_susceptibility = mongoDB.DynamicField(required=True)
    plant_pathogen = mongoDB.DynamicField(required=True)
    optimal_temperature = mongoDB.DynamicField(required=True)
    optimal_ph = mongoDB.DynamicField(required=True)
    animal_pathogen = mongoDB.DynamicField(required=True)
    microbiome_location = mongoDB.DynamicField(required=True)
    biofilm_forming = mongoDB.DynamicField(required=True)
    spore_forming = mongoDB.DynamicField(required=True)
    pathogenicity = mongoDB.DynamicField(required=True)
    extreme_environment = mongoDB.DynamicField(required=True)
    gram_stain = mongoDB.DynamicField(required=True)


class MicrobeDirectoryResultModule(ToolResultModule):
    """Microbe Directory tool module."""

    @classmethod
    def name(cls):
        """Return Microbe Directory module's unique identifier string."""
        return 'microbe_directory_annotate'

    @classmethod
    def result_model(cls):
        """Return Microbe Directory module's model class."""
        return MicrobeDirectoryResult

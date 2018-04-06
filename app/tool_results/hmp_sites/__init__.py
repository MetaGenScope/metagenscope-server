"""HMP Sites tool module."""

from mongoengine import ValidationError

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule

from .constants import MODULE_NAME


class HmpSitesResult(ToolResult):       # pylint: disable=too-few-public-methods
    """HMP Sites tool's result type."""

    # We do not provide a default=0 because 0 is a valid cosine similarity value
    skin = mongoDB.ListField(mongoDB.FloatField())
    oral = mongoDB.ListField(mongoDB.FloatField())
    urogenital = mongoDB.ListField(mongoDB.FloatField())
    airways = mongoDB.ListField(mongoDB.FloatField())

    def clean(self):
        """Check that all vals are in range [0, 1] if not then error."""
        def validate(*vals):
            """Confirm values are in range [0,1], if they exist."""
            for value_list in vals:
                for value in value_list:
                    if value is not None and (value < 0 or value > 1):
                        return False
            return True

        if not validate(self.skin,
                        self.oral,
                        self.urogenital,
                        self.airways):
            msg = 'HMPSitesResult values in bad range'
            raise ValidationError(msg)

    @staticmethod
    def site_names(self):
        """Return the names of the body sites."""
        return ['skin', 'oral', 'urogenital', 'airways']


class HmpSitesResultModule(ToolResultModule):
    """HMP Sites tool module."""

    @classmethod
    def name(cls):
        """Return HMP Sites module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return HMP Sites module's model class."""
        return HmpSitesResult

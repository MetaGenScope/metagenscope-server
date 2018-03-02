"""HMP Sites tool module."""
from mongoengine import ValidationError

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class HmpSitesResult(ToolResult):       # pylint: disable=too-few-public-methods
    """HMP Sites tool's result type."""

    gut = mongoDB.FloatField()
    skin = mongoDB.FloatField()
    throat = mongoDB.FloatField()
    urogenital = mongoDB.FloatField()
    airways = mongoDB.FloatField()

    def clean(self):
        def validate(*vals):
            for val in vals:
                if (val > 1) or (val < 0):
                    return False
                return True

        if not validate(self.gut,
                        self.skin,
                        self.throat,
                        self.urogenital,
                        self.airways):
            msg = f'HMPSitesResult values in bad range'
            raise ValidationError(msg)


class HmpSitesResultModule(ToolResultModule):
    """HMP Sites tool module."""

    @classmethod
    def name(cls):
        """Return HMP Sites module's unique identifier string."""
        return 'hmp_sites'

    @classmethod
    def result_model(cls):
        """Return HMP Sites module's model class."""
        return HmpSitesResult

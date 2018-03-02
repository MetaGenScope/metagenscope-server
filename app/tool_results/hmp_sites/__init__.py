"""HMP Sites tool module."""

from mongoengine import ValidationError

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class HmpSitesResult(ToolResult):       # pylint: disable=too-few-public-methods
    """HMP Sites tool's result type."""

    # We do not provide a default=0 because 0 is a valid cosine similarity value
    gut = mongoDB.FloatField()
    skin = mongoDB.FloatField()
    throat = mongoDB.FloatField()
    urogenital = mongoDB.FloatField()
    airways = mongoDB.FloatField()

    def clean(self):
        """Check that all vals are in range [0, 1] if not then error."""
        def validate(*vals):
            """Confirm values are in range [0,1], if they exist."""
            for val in vals:
                if val is not None and (val < 0 or val > 1):
                    return False
            return True

        if not validate(self.gut,
                        self.skin,
                        self.throat,
                        self.urogenital,
                        self.airways):
            msg = 'HMPSitesResult values in bad range'
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

    @classmethod
    def make_result_model(cls, post_json):
        """Process uploaded JSON (if necessary) and create result model."""
        return cls.result_model()(**post_json)

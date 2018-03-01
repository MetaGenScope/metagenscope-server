"""Base module for Tool Results."""

from app.extensions import mongoDB


class ToolResult(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Base mongo result class."""

    # Turns out there isn't much in common between ToolResult types...

    meta = {'abstract': True}


class ToolResultModule:
    """Base module for Tool Results."""

    @classmethod
    def name(cls):
        """Return Tool Result module's unique identifier string."""
        raise NotImplementedError()

    @classmethod
    def result_model(cls):
        """Return the Tool Result module's model class."""
        raise NotImplementedError()

"""Base module for Group Tool Results."""


class BaseToolResultModule:
    """Base module for Group Tool Results."""

    @classmethod
    def name(cls):
        """Return Tool Result module's unique identifier string."""
        raise NotImplementedError('ToolResultModule subclass must override')

    @classmethod
    def endpoint(cls):
        """Return Tool Result module's API upload endpoint."""
        raise NotImplementedError('ToolResultModule subclass must override')

    @classmethod
    def result_model(cls):
        """Return the Tool Result module's model class."""
        raise NotImplementedError('ToolResultModule subclass must override')

    @classmethod
    def make_result_model(cls, payload):
        """Process uploaded JSON (if necessary) and create result model."""
        result_model_cls = cls.result_model()
        result_model = result_model_cls(**payload)
        return result_model

    @classmethod
    def upload_hooks(cls):
        """Return a list of functions to be called on uploaded json."""
        return []

    @classmethod
    def run_upload_hooks(cls, payload):
        """Run a set of upload hooks on the given payload and return the result."""
        for hook in cls.upload_hooks():
            payload = hook(payload)
        return payload


class SampleToolResultModule(BaseToolResultModule):
    """Base module for Sample Tool Results."""

    @classmethod
    def name(cls):
        """Return Sample Tool Result module's unique identifier string."""
        raise NotImplementedError('SampleToolResultModule subclass must override')

    @classmethod
    def result_model(cls):
        """Return the Sample Tool Result module's model class."""
        raise NotImplementedError('SampleToolResultModule subclass must override')

    @classmethod
    def endpoint(cls):
        """Return Sample Tool Result module's API upload endpoint."""
        return f'/samples/<uuid>/{cls.name()}'


class GroupToolResultModule(BaseToolResultModule):
    """Base module for Group Tool Results."""

    @classmethod
    def name(cls):
        """Return Group Tool Result module's unique identifier string."""
        raise NotImplementedError('GroupToolResultModule subclass must override')

    @classmethod
    def result_model(cls):
        """Return the Group Tool Result module's model class."""
        raise NotImplementedError('GroupToolResultModule subclass must override')

    @classmethod
    def endpoint(cls):
        """Return Tool Result module's API upload endpoint."""
        return f'/sample_groups/<uuid>/{cls.name()}'

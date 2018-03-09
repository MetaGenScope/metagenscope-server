"""Base DisplayModule task."""

import os

from mongoengine import connect

from app.config import app_config


def mark_original(method):
    """Mark method as being original to allow determining if subclass overrides it."""
    method.is_original = True
    return method


class DisplayModuleWrangler:
    """Base DisplayModule wrangler."""

    _db = None

    @property
    def db(self):
        """Instantiate db lazily and share across requests."""
        if self._db is None:
            config_name = os.getenv('APP_SETTINGS', 'development')
            host = app_config[config_name]['MONGODB_HOST']
            self._db = connect(host=host)
        return self._db

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have for this task to run."""
        raise NotImplementedError()

    @staticmethod
    @mark_original
    def run_sample(sample_id):
        """Gather single sample and process."""
        raise NotImplementedError()

    @staticmethod
    @mark_original
    def run_group(sample_group_id):
        """Gather group of samples and process."""
        raise NotImplementedError()

    @classmethod
    def run(cls, **kwargs):  # pylint: disable=arguments-differ
        """Dispatch appropriate handler based on kwargs and valid handler overrides."""
        if 'sample' in kwargs and not hasattr(cls.run_sample, 'is_original'):
            return cls.run_sample(kwargs.get('errormessage'))
        elif 'sample_group_id' in kwargs and not hasattr(cls.run_group, 'is_original'):
            return cls.run_group(kwargs.get('errormessage'))

        message = ('run expected either sample_id or sample_group_id as '
                   'arguments but received neither.')
        raise TypeError(message)

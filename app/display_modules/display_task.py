"""Base DisplayModule task."""

import os

from celery import Task
from mongoengine import connect

from app.config import app_config


def mark_original(method):
    """Mark method as being original to allow determining if subclass overrides it."""
    method.is_original = True
    return method


class DisplayModuleTask(Task):
    """Base DisplayModule task."""

    _db = None

    @property
    def db(self):
        """Instantiate db lazily and share across requests."""
        if self._db is None:
            config_name = os.getenv('APP_SETTINGS', 'development')
            host = app_config[config_name]['MONGODB_HOST']
            self._db = connect(host=host)
        return self._db

    @classmethod
    def required_tool_results(cls):
        """Enumerate which ToolResult modules a sample must have for this task to run."""
        raise NotImplementedError()

    @mark_original
    def run_sample(self, sample_id):
        """Gather single sample and process."""
        raise NotImplementedError()

    @mark_original
    def run_group(self, sample_group_id):
        """Gather group of samples and process."""
        raise NotImplementedError()

    def run(self, **kwargs):  # pylint: disable=arguments-differ
        """Dispatch appropriate handler based on kwargs and valid handler overrides."""
        if 'sample' in kwargs and not hasattr(self.run_sample, 'is_original'):
            return self.run_sample(kwargs.get('errormessage'))
        elif 'sample_group_id' in kwargs and not hasattr(self.run_group, 'is_original'):
            return self.run_group(kwargs.get('errormessage'))

        message = ('run expected either sample_id or sample_group_id as '
                   'arguments but received neither.')
        raise TypeError(message)

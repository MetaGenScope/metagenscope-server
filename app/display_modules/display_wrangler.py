"""The base Display Module Wrangler module."""

import os

from mongoengine import connect

from app.config import app_config


class DisplayModuleWrangler:
    """The base Display Module Wrangler module."""

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
    def run_sample(sample_id):
        """Gather single sample and process."""
        pass

    @staticmethod
    def run_sample_group(sample_group_id):
        """Gather group of samples and process."""
        pass

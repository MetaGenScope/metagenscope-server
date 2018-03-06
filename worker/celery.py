"""Asynchronous worker application."""

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from app.display_modules import all_display_modules
from worker.config import app_config


def create_app():
    """Create and bootstrap worker app."""
    # Instantiate the app
    app = Celery('metagenscope')

    # Set configuration
    config_name = os.getenv('APP_SETTINGS', 'development')
    app.conf.update(app_config[config_name])

    register_task_list(app)

    return app


def register_task_list(app):
    """Register list of tasks based on display modules."""
    tasks = []
    for module in all_display_modules:
        # TODO: register all tasks for module
        print(module)
    app.conf.include = tuple(tasks)

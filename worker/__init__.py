"""
Asynchronous worker application for processing MetaGenScope queries.

Celery w/ Flask facory pattern from:
  https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern

  - The app.app_context().push() caused some problems with automated testing of
    module loading. Adjusted tests to exclude ./worker. This shouldn't cause issues
    running the Flask app as `worker` is never imported.
"""

from app import create_app
from app.extensions import celery

app = create_app()
app.app_context().push()

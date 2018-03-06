"""Asynchronous worker application for processing MetaGenScope queries."""

from worker.celery import create_app

celery = create_app()  # pylint: disable=invalid-name

if __name__ == '__main__':
    celery.start()

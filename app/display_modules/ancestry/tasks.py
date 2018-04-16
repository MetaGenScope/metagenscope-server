"""Tasks for generating Microbe Directory results."""

from app.extensions import celery

from .models import MicrobeDirectoryResult


@celery.task()
def microbe_directory_reducer(samples):
    """Wrap collated samples as actual Result type."""
    return MicrobeDirectoryResult(samples=samples)

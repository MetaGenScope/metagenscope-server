"""Tasks to process Alpha Diversity results."""

from app.extensions import celery
from app.display_modules.utils import persist_result_helper

from .models import AncestryResult


@celery.task(name='ancestry.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Beta Diversity results."""
    result = AncestryResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)

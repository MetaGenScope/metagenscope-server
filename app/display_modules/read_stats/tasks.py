"""Read Stats wrangler and related."""

from app.extensions import celery
from app.display_modules.utils import persist_result_helper

from .models import ReadStatsResult


@celery.task()
def read_stats_reducer(samples):
    """Wrap collated samples as actual Result type."""
    result_data = {'samples': samples}
    return result_data


@celery.task(name='read_stats.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Read Stats results."""
    result = ReadStatsResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)

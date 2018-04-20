"""Tasks for generating Reads Classified results."""

from celery import chain

from app.extensions import celery
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import collate_samples, persist_result_helper

from .constants import MODULE_NAME, TOOL_MODULE_NAME
from .models import ReadsClassifiedResult


@celery.task(name='reads_classified.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Reads Classified result."""
    result = ReadsClassifiedResult(samples=result_data)
    persist_result_helper(result, analysis_result_id, result_name)


class ReadsClassifiedWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather and process a single sample."""
        pass

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        collate_fields = ['viral', 'archaea', 'bacteria', 'host', 'unknown']
        collate_task = collate_samples.s(TOOL_MODULE_NAME, collate_fields, samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)

        task_chain = chain(collate_task, persist_task)
        result = task_chain.delay()

        return result

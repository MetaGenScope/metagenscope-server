"""Tasks for generating Reads Classified results."""

import celery
from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import collate_samples, persist_result
from app.sample_groups.sample_group_models import SampleGroup

from .constants import MODULE_NAME, TOOL_MODULE_NAME
from .models import ReadsClassifiedResult


@celery.task
def reducer_task(samples):
    """Return an HMP result model from components."""
    return ReadsClassifiedResult(samples=samples)


class ReadsClassifiedWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    @classmethod
    def run_sample(cls, sample_id):
        """Gather and process a single sample."""
        pass

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.analysis_result.set_module_status(MODULE_NAME, 'W')

        collate_task = collate_samples.s(
            TOOL_MODULE_NAME,
            ['viral', 'archaea', 'bacteria', 'host', 'unknown'],
            sample_group_id
        )
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)
        task_chain = chain(
            collate_task,
            reducer_task.s(),
            persist_task,
        )
        result = task_chain.delay()

        return result

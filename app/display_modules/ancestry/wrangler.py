"""Wrangler for Ancestry results."""

from celery import chain
from pandas import DataFrame

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result, collate_samples
from app.extensions import celery
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.ancestry import AncestryToolResult

from .constants import MODULE_NAME, TOOL_MODULE_NAME
from .models import AncestryResult


@celery.task()
def ancestry_reducer(samples):
    """Wrap collated samples as actual Result type."""
    samples = DataFrame().fillna(val=0).to_dict()
    return AncestryResult(samples=samples)


class AncestryWrangler(DisplayModuleWrangler):
    """Tasks for generating ancestry results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.analysis_result.set_module_status(MODULE_NAME, 'W')

        collate_fields = AncestryToolResult._fields
        collate_task = collate_samples.s(TOOL_MODULE_NAME, collate_fields, sample_group_id)
        reducer_task = ancestry_reducer.s()
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, reducer_task, persist_task)
        result = task_chain.delay()

        return result

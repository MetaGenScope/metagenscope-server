"""Wrangler for Ancestry results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import collate_samples
from app.tool_results.ancestry import AncestryToolResult

from .constants import MODULE_NAME, TOOL_MODULE_NAME
from .tasks import ancestry_reducer, persist_result


class AncestryWrangler(DisplayModuleWrangler):
    """Tasks for generating ancestry results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        collate_fields = list(AncestryToolResult._fields.keys())
        collate_task = collate_samples.s(TOOL_MODULE_NAME, collate_fields, samples)
        reducer_task = ancestry_reducer.s()
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, reducer_task, persist_task)
        result = task_chain.delay()

        return result

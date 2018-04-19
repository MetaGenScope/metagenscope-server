"""Wrangler for Microbe Directory results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import collate_samples
from app.tool_results.microbe_directory import (
    MicrobeDirectoryToolResult,
    MicrobeDirectoryResultModule,
)

from .constants import MODULE_NAME
from .tasks import microbe_directory_reducer, persist_result


class MicrobeDirectoryWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        tool_result_name = MicrobeDirectoryResultModule.name()
        collate_fields = list(MicrobeDirectoryToolResult._fields.keys())
        collate_task = collate_samples.s(tool_result_name, collate_fields, samples)
        reducer_task = microbe_directory_reducer.s()
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, reducer_task, persist_task)
        result = task_chain.delay()

        return result

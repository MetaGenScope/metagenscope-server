"""Wrangler for Microbe Directory results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import jsonify, persist_result, collate_samples
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.microbe_directory import (
    MicrobeDirectoryToolResult,
    MicrobeDirectoryResultModule,
)

from .constants import MODULE_NAME
from .tasks import microbe_directory_reducer


class MicrobeDirectoryWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.analysis_result.set_module_status(MODULE_NAME, 'W')
        samples = jsonify(sample_group.samples)

        tool_result_name = MicrobeDirectoryResultModule.name()
        collate_fields = MicrobeDirectoryToolResult._fields
        collate_task = collate_samples.s(tool_result_name, collate_fields, samples)
        reducer_task = microbe_directory_reducer.s()
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, reducer_task, persist_task)
        result = task_chain.delay()

        return result

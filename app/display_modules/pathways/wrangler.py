"""Tasks for generating Pathway results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result
from app.sample_groups.sample_group_models import SampleGroup

from .constants import MODULE_NAME
from .tasks import filter_humann2_pathways


class PathwayWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather samples and process."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.analysis_result.set_module_status(MODULE_NAME, 'W')

        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        task_chain = chain(filter_humann2_pathways.s(sample_group.samples),
                           persist_task)
        result = task_chain.delay()

        return result

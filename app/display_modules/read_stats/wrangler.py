"""Read Stats wrangler and related."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result, collate_samples
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.read_stats import ReadStatsToolResultModule

from .constants import MODULE_NAME
from .models import ReadStatsResult


class ReadStatsWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        analysis_group = cls.set_analysis_group_state(MODULE_NAME, sample_group)

        collate_task = collate_samples.s(ReadStatsToolResultModule.name(),
                                         ['raw', 'microbial'],
                                         sample_group_id,
                                         ReadStatsResult)
        persist_task = persist_result.s(analysis_group.uuid, MODULE_NAME)

        task_chain = chain(collate_task, persist_task)
        result = task_chain.delay()

        return result

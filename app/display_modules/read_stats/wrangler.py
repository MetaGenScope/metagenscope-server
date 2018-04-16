"""Read Stats wrangler and related."""

from celery import chain

from app.extensions import celery
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import jsonify, persist_result, collate_samples
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.read_stats import ReadStatsToolResultModule

from .constants import MODULE_NAME
from .models import ReadStatsResult


@celery.task()
def read_stats_reducer(samples):
    """Wrap collated samples as actual Result type."""
    return ReadStatsResult(samples=samples)


class ReadStatsWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.analysis_result.set_module_status(MODULE_NAME, 'W')
        analysis_group = sample_group.analysis_result
        samples = jsonify(sample_group.samples)

        collate_task = collate_samples.s(ReadStatsToolResultModule.name(),
                                         ['raw', 'microbial'],
                                         samples)
        persist_task = persist_result.s(analysis_group.uuid, MODULE_NAME)

        task_chain = chain(collate_task,
                           read_stats_reducer.s(),
                           persist_task)
        result = task_chain.delay()

        return result

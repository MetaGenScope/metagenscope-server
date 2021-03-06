"""Tasks for generating AGS results."""

from celery import chord

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata

from .ags_tasks import ags_distributions, reducer_task, persist_result


class AGSWrangler(DisplayModuleWrangler):
    """Tasks for generating AGS results."""

    @staticmethod
    def run_sample_group(sample_group, samples):
        """Gather samples then process them."""
        reducer = reducer_task.s()
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        'average_genome_size')
        categories_task = categories_from_metadata.s(samples)
        ags_distribution_task = ags_distributions.s(samples)
        middle_tasks = [categories_task, ags_distribution_task]

        return chord(middle_tasks)(reducer | persist_task)

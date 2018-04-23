"""Task for generating Taxon Abundance results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler

from .constants import MODULE_NAME
from .tasks import make_all_flows, persist_result


class TaxonAbundanceWrangler(DisplayModuleWrangler):
    """Task for generating Taxon Abundance results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        flow_task = make_all_flows.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)
        task_chain = chain(
            flow_task,
            persist_task,
        )
        result = task_chain.delay()

        return result

"""Taxa Tree wrangler and related."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result
from app.samples.sample_models import Sample

from .constants import MODULE_NAME
from .tasks import trees_from_sample, taxa_tree_reducer


class TaxaTreeWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample(cls, sample_id):
        """Make taxa trees for a given sample."""
        sample = Sample.objects.get(uuid=sample_id)
        sample.analysis_result.fetch().set_module_status(MODULE_NAME, 'W')

        persist_task = persist_result.s(sample.analysis_result.pk, MODULE_NAME)

        task_chain = chain(
            trees_from_sample.s(sample),
            taxa_tree_reducer.s(),
            persist_task
        )

        result = task_chain.delay()
        return result

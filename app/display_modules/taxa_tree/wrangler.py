"""Taxa Tree wrangler and related."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import jsonify

from .constants import MODULE_NAME
from .tasks import trees_from_sample, persist_result


class TaxaTreeWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        safe_sample = jsonify(sample)
        tree_task = trees_from_sample.s(safe_sample)
        persist_task = persist_result.s(sample.analysis_result.pk, MODULE_NAME)

        task_chain = chain(tree_task, persist_task)
        result = task_chain.delay()

        return result

"""Tasks for generating HMP results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import jsonify, categories_from_metadata, persist_result
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup

from .constants import MODULE_NAME
from .tasks import make_distributions, reducer_task


class HMPWrangler(DisplayModuleWrangler):
    """Task for generating HMP results."""

    @classmethod
    def run_sample(cls, sample_id):
        """Gather single sample and process."""
        sample = Sample.objects.get(uuid=sample_id)
        sample.analysis_result.fetch().set_module_status(MODULE_NAME, 'W')

        samples = [jsonify(sample)]
        categories_task = categories_from_metadata.s(samples, min_size=1)
        distribution_task = make_distributions.s(samples)
        persist_task = persist_result.s(sample.analysis_result.pk,
                                        MODULE_NAME)

        task_chain = chain(categories_task, distribution_task, reducer_task.s(), persist_task)
        result = task_chain.delay()

        return result

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.analysis_result.set_module_status(MODULE_NAME, 'W')
        samples = jsonify(sample_group.samples)

        categories_task = categories_from_metadata.s(samples, min_size=1)
        distribution_task = make_distributions.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)
        task_chain = chain(
            categories_task,
            distribution_task,
            reducer_task.s(),
            persist_task,
        )
        result = task_chain.delay()

        return result

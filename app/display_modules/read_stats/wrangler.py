"""Read Stats wrangler and related."""

from celery import chain

from app.extensions import mongoDB as mdb
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result, collate_samples
from app.sample_groups.sample_group_models import SampleGroup


MODULE_NAME = 'read_stats'


class ReadStatsResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    samples = mdb.MapField(field=mdb.DynamicField(), required=True)


class ReadStatsWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    collate_task = collate_samples.s(['raw', 'microbial'])

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.set_module_status(sample_group, MODULE_NAME, 'W')

        persist_task = persist_result.s(sample_group.analysis_group_uuid, MODULE_NAME)

        task_chain = chain(cls.collate_task.s(sample_group.samples), persist_task)
        result = task_chain().delay()

        return result

"""Tasks for generating Pathway results."""

from celery import chain

from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result
from app.sample_groups.sample_group_models import SampleGroup

from .constants import MODULE_NAME
from .tasks import filter_humann2_pathways


class PathwayWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    humann2_task = filter_humann2_pathways.s()

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather samples and process."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()

        # Set state on Analysis Group
        analysis_group = sample_group.analysis_result
        wrapper = AnalysisResultWrapper(status='W')
        setattr(analysis_group, MODULE_NAME, wrapper)
        analysis_group.save()

        persist_task = persist_result.s(analysis_group.uuid, MODULE_NAME)

        task_chain = chain(cls.humann2_task.s(sample_group.samples), persist_task)
        result = task_chain.delay()

        return result

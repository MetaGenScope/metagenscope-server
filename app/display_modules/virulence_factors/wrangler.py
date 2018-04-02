"""Tasks for generating Virulence Factor results."""

from celery import chain

from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result
from app.sample_groups.sample_group_models import SampleGroup

from .constants import MODULE_NAME
from .tasks import filter_vfdb_results


class VFDBWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):  # pylint: disable=duplicate-code
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()

        # Set state on Analysis Group
        analysis_result = sample_group.analysis_result
        wrapper = AnalysisResultWrapper(status='W')
        setattr(analysis_result, MODULE_NAME, wrapper)
        analysis_result.save()

        filter_vfdb_task = filter_vfdb_results.s(sample_group.samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)

        task_chain = chain(filter_vfdb_task, persist_task)
        result = task_chain().get()

        return result

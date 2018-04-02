"""Tasks for generating Virulence Factor results."""

from celery import chain

from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result
from app.sample_groups.sample_group_models import SampleGroup

from .tasks import filter_gene_results


class GenericGeneWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def help_run_sample_group(cls, result_name, result_type, top_n, sample_group_id):  # pylint: disable=duplicate-code
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()

        # Set state on Analysis Group
        analysis_result = sample_group.analysis_result
        wrapper = AnalysisResultWrapper(status='W')
        setattr(analysis_result, result_name, wrapper)
        analysis_result.save()

        filter_gene_task = filter_gene_results.s(sample_group.samples,
                                                 result_name, result_type,
                                                 top_n)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        result_name)

        task_chain = chain(filter_gene_task, persist_task)
        result = task_chain().get()

        return result

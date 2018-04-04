"""Tasks for generating Virulence Factor results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result
from app.sample_groups.sample_group_models import SampleGroup

from .tasks import filter_gene_results


class GenericGeneWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    tool_result_name = None
    result_name = None

    @classmethod
    def help_run_sample_group(cls, result_type, top_n, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        analysis_result = cls.set_analysis_group_status(cls.result_name,
                                                        sample_group)

        filter_task = filter_gene_results.s(sample_group.samples,
                                            cls.tool_result_name,
                                            result_type,
                                            top_n)
        persist_task = persist_result.s(analysis_result.uuid, cls.result_name)

        task_chain = chain(filter_task, persist_task)
        result = task_chain.delay()
        assert result is not None
        return result

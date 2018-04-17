"""Tasks for generating Virulence Factor results."""

from app.extensions import celery
from app.display_modules.generic_gene_set.wrangler import GenericGeneWrangler
from app.display_modules.utils import persist_result_helper

from .models import VFDBResult
from .constants import MODULE_NAME, TOP_N


@celery.task(name='vfdb.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist VFDB results."""
    result = VFDBResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)


class VFDBWrangler(GenericGeneWrangler):
    """Tasks for generating virulence results."""

    tool_result_name = 'vfdb_quantify'
    result_name = MODULE_NAME

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        result = cls.help_run_sample_group(sample_group_id, TOP_N, persist_result)
        return result

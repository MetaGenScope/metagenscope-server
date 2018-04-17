"""Tasks for generating CARD AMR results."""

from app.extensions import celery
from app.display_modules.generic_gene_set.wrangler import GenericGeneWrangler
from app.display_modules.utils import persist_result_helper
from app.tool_results.card_amrs.constants import MODULE_NAME as TOOL_MODULE_NAME

from .models import CARDGenesResult
from .constants import MODULE_NAME, TOP_N


@celery.task(name='card_amrs.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist CARD AMRS results."""
    result = CARDGenesResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)


class CARDGenesWrangler(GenericGeneWrangler):
    """Tasks for generating virulence results."""

    tool_result_name = TOOL_MODULE_NAME
    result_name = MODULE_NAME

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        result = cls.help_run_sample_group(sample_group_id, TOP_N, persist_result)
        return result

"""Wrangler for generating Methyl results."""

from app.display_modules.generic_gene_set.wrangler import GenericGeneWrangler

from .models import MethylResult
from .constants import MODULE_NAME, TOP_N


class MethylWrangler(GenericGeneWrangler):
    """Tasks for generating methyls results."""

    tool_result_name = 'align_to_methyltransferases'
    result_name = MODULE_NAME
    result_type = MethylResult

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        result = cls.help_run_sample_group(TOP_N, sample_group_id)
        return result

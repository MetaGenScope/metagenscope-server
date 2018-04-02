"""Wrangler for generating Methyl results."""

from app.display_modules.generic_gene_set.wrangler import GenericGeneWrangler

from .models import MethylResult
from .constants import MODULE_NAME, TOP_N


class MethylWrangler(GenericGeneWrangler):
    """Tasks for generating methyls results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        result = cls.help_run_sample_group(MODULE_NAME, MethylResult,
                                           TOP_N, sample_group_id)
        return result

# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Functional Genes models for testing."""

from app.display_modules.generic_gene_set.tests.factory import GeneSetFactory
from app.display_modules.functional_genes import FunctionalGenesResult


class FunctionalGenesFactory(GeneSetFactory):
    """Factory for Analysis Result's Functional Genes."""

    class Meta:
        """Factory metadata."""

        model = FunctionalGenesResult

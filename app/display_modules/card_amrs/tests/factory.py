# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

from app.display_modules.generic_gene_set.tests.factory import GeneSetFactory
from app.display_modules.card_amrs import CARDGenesResult


class CARDGenesFactory(GeneSetFactory):
    """Factory for CARD Genes."""

    class Meta:
        """Factory metadata."""

        model = CARDGenesResult

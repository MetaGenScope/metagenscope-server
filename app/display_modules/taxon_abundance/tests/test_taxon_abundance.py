"""Test suite for Taxon Abundance model."""

from mongoengine import ValidationError

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.taxon_abundance import TaxonAbundanceResult
from tests.base import BaseTestCase


def flow_model():
    """Return an example flow model."""
    return {
        'nodes': [
            {
                'id': 'left_root',
                'name': 'left_root',
                'value': 3.5,
            },
            {
                'id': 'right_root',
                'name': 'right_root',
                'value': 3.5,
            },
        ], 'edges': [
            {
                'source': 'left_root',
                'target': 'right_root',
                'value': 1.0,
            },
        ]
    }


class TestTaxonAbundanceResult(BaseTestCase):
    """Test suite for Taxon Abundance model."""

    def test_add_taxon_abundance(self):
        """Ensure Taxon Abundance model is created correctly."""
        taxon_abundance = TaxonAbundanceResult(kraken=flow_model(), metaphlan2=flow_model())
        wrapper = AnalysisResultWrapper(data=taxon_abundance)
        result = AnalysisResultMeta(taxon_abundance=wrapper).save()
        self.assertTrue(result.id)
        self.assertTrue(result.taxon_abundance)

    def test_add_missing_node(self):
        """Ensure saving model fails if edge references missing node."""
        taxon_abundance = TaxonAbundanceResult(kraken=flow_model(), metaphlan2=flow_model())
        wrapper = AnalysisResultWrapper(data=taxon_abundance)
        result = AnalysisResultMeta(taxon_abundance=wrapper)
        self.assertRaises(ValidationError, result.save)

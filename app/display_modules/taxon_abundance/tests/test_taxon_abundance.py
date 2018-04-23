"""Test suite for Taxon Abundance model."""

from mongoengine import ValidationError

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.taxon_abundance import TaxonAbundanceResult
from app.display_modules.taxon_abundance.wrangler import TaxonAbundanceWrangler
from app.samples.sample_models import Sample
from app.tool_results.kraken.tests.factory import create_taxa
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

    def test_get_read_stats(self):
        """Ensure getting a single TaxonAbundance behaves correctly."""
        taxon_abundance = TaxonAbundanceResult(kraken=flow_model(), metaphlan2=flow_model())
        self.generic_getter_test(taxon_abundance, MODULE_NAME)

    def test_run_read_stats_sample_group(self):  # pylint: disable=invalid-name
        """Ensure TaxonAbundance run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          kraken=create_taxa(),
                          metaphlan2=create_taxa()).save()

        self.generic_run_group_test(create_sample,
                                    TaxonAbundanceWrangler,
                                    MODULE_NAME)

"""Test suite for Taxa Tree display module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.read_stats.wrangler import ReadStatsWrangler
from app.display_modules.read_stats.models import ReadStatsResult
from app.display_modules.read_stats.constants import MODULE_NAME
from app.display_modules.read_stats.tests.factory import ReadStatsFactory
from app.samples.sample_models import Sample
from app.tool_results.read_stats.tests.factory import (
    create_read_stats,
    create_values
)


class TestTaxaTreeModule(BaseDisplayModuleTest):
    """Test suite for ReadStats diplay module."""

    def test_get_taxa_tree(self):
        """Ensure getting a single TaxaTree behaves correctly."""
        ttree = TaxaTreeFactory()
        self.generic_getter_test(ttree, MODULE_NAME)

    def test_add_taxa_tree(self):
        """Ensure TaxaTree model is created correctly."""
        samples = {
            'metaphlan2': generate_random_tree(),
            'kraken': generate_random_tree(),
        }
        taxa_tree_result = TaxaTreeResult(samples=samples)
        self.generic_adder_test(taxa_tree_result, MODULE_NAME)

    def test_run_taxa_tree_sample(self):  # pylint: disable=invalid-name
        """Ensure ReadStats run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_read_stats()
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          read_stats=data).save()

        self.generic_run_group_test(create_sample,
                                    ReadStatsWrangler,
                                    MODULE_NAME)

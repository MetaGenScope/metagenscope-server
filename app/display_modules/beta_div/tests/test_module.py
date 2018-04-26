"""Test suite for Beta Diversity display module."""

from app.display_modules.beta_div.models import BetaDiversityResult
from app.display_modules.beta_div import MODULE_NAME
from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.tool_results.beta_diversity.tests.factory import create_ranks

from .factory import BetaDiversityFactory


class TestBetaDivModule(BaseDisplayModuleTest):
    """Test suite for Beta Diversity diplay module."""

    def test_add_beta_div(self):
        """Ensure Beta Diversity model is created correctly."""
        ranks = create_ranks()
        beta_div_result = BetaDiversityResult(data=ranks)
        self.generic_adder_test(beta_div_result, MODULE_NAME)

    def test_get_beta_div(self):
        """Ensure getting a single Beta Diversity behaves correctly."""
        ranks = create_ranks()
        beta_div_result = BetaDiversityFactory()
        self.generic_getter_test(beta_div_result, MODULE_NAME,
                                 verify_fields=('data',))

    def test_run_beta_div_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Beta Diversity run_sample_group produces correct results."""
        pass

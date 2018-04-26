"""Test suite for Alpha Diversity tool result model."""

from app.tool_results.alpha_diversity import AlphaDiversityResultModule
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestAlphaDivModel(BaseToolResultTest):
    """Test suite for Alpha Div tool result model."""

    def test_add_alpha_div(self):
        """Ensure Alpha Div tool result model is created correctly."""

        alpha_diversity = AlphaDiversityResultModule.result_model()(**create_values())
        self.generic_add_test(alpha_diversity, AlphaDiversityResultModule.name())

    def test_upload_alpha_div(self):
        """Ensure a raw Alpha Div tool result can be uploaded."""

        self.generic_test_upload(create_values(),
                                 AlphaDiversityResultModule.name())

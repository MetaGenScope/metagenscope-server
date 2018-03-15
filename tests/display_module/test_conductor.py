"""Test suite for DisplayModuleConductor."""

from uuid import uuid4

from app.display_modules.conductor import DisplayModuleConductor
from app.display_modules.sample_similarity import SampleSimilarityDisplayModule
from app.tool_results.kraken import KrakenResultModule
from tests.base import BaseTestCase


class TestConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    def test_downstream_modules(self):
        """Ensure downstream_modules is computed correctly."""
        sample_id = str(uuid4())
        conductor = DisplayModuleConductor(sample_id, KrakenResultModule)
        self.assertIn(SampleSimilarityDisplayModule, conductor.downstream_modules)

    def test_get_valid_modules(self):
        """Ensure valid_modules is computed correctly."""
        tools_present = set(['kraken', 'metaphlan2'])
        sample_id = str(uuid4())
        conductor = DisplayModuleConductor(sample_id, KrakenResultModule)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertIn(SampleSimilarityDisplayModule, valid_modules)

    def test_partial_valid_modules(self):
        """Ensure valid_modules is computed correctly if tools are missing."""
        tools_present = set(['kraken'])
        sample_id = str(uuid4())
        conductor = DisplayModuleConductor(sample_id, KrakenResultModule)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertTrue(SampleSimilarityDisplayModule not in valid_modules)

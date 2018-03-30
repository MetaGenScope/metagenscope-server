"""Test suite for DisplayModuleConductor."""

from uuid import uuid4

from app.display_modules.conductor import DisplayModuleConductor
from app.display_modules.sample_similarity import SampleSimilarityDisplayModule
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from tests.base import BaseTestCase


KRAKEN_NAME = KrakenResultModule.name()
METAPHLAN2_NAME = Metaphlan2ResultModule.name()


class TestConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    def test_downstream_modules(self):
        """Ensure downstream_modules is computed correctly."""
        sample_id = str(uuid4())
        conductor = DisplayModuleConductor(sample_id, KrakenResultModule)
        self.assertIn(SampleSimilarityDisplayModule, conductor.downstream_modules)

    def test_get_valid_modules(self):
        """Ensure valid_modules is computed correctly."""
        tools_present = set([KRAKEN_NAME, METAPHLAN2_NAME])
        sample_id = str(uuid4())
        conductor = DisplayModuleConductor(sample_id, KrakenResultModule)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertIn(SampleSimilarityDisplayModule, valid_modules)

    def test_partial_valid_modules(self):
        """Ensure valid_modules is computed correctly if tools are missing."""
        tools_present = set([KRAKEN_NAME])
        sample_id = str(uuid4())
        conductor = DisplayModuleConductor(sample_id, KrakenResultModule)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertTrue(SampleSimilarityDisplayModule not in valid_modules)

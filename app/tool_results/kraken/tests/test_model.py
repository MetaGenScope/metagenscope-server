"""Test suite for Kraken tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.kraken import KrakenResultModule, KrakenResult
from app.tool_results.kraken.tests.constants import TEST_TAXA

from tests.base import BaseTestCase

KRAKEN_NAME = KrakenResultModule.name()


class TestKrakenModel(BaseTestCase):
    """Test suite for Kraken tool result model."""

    def test_add_kraken_result(self):
        """Ensure Kraken result model is created correctly."""
        sample_data = {'name': 'SMPL_01', KRAKEN_NAME: KrakenResult(taxa=TEST_TAXA)}
        sample = Sample(**sample_data).save()
        self.assertTrue(hasattr(sample, KRAKEN_NAME))
        tool_result = getattr(sample, KRAKEN_NAME)
        self.assertEqual(len(tool_result.taxa), 6)
        self.assertEqual(tool_result.taxa['d__Viruses'], 1733)
        self.assertEqual(tool_result.taxa['d__Bacteria'], 7396285)
        self.assertEqual(tool_result.taxa['d__Archaea'], 12)
        self.assertEqual(tool_result.taxa['d__Bacteria|p__Proteobacteria'], 7285377)
        self.assertEqual(tool_result.taxa['d__Archaea|p__Euryarchaeota|c__Methanomicrobia'], 2)
        self.assertEqual(tool_result.taxa['d__Viruses|o__Caudovirales'], 1694)

"""Test suite for Metaphlan 2 tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.metaphlan2 import Metaphlan2Result
from app.tool_results.metaphlan2.tests.constants import TEST_TAXA

from tests.base import BaseTestCase


class TestMetaphlan2Model(BaseTestCase):
    """Test suite for Metaphlan 2 tool result model."""

    def test_add_metaphlan2_result(self):
        """Ensure Metaphlan 2 result model is created correctly."""

        metaphlan2 = Metaphlan2Result(taxa=TEST_TAXA)
        sample = Sample(name='SMPL_01', metaphlan2=metaphlan2).save()
        self.assertTrue(sample.metaphlan2)
        metaphlan_result = sample.metaphlan2
        self.assertEqual(len(metaphlan_result.taxa), 6)
        self.assertEqual(metaphlan_result.taxa['d__Viruses'], 1733)
        self.assertEqual(metaphlan_result.taxa['d__Bacteria'], 7396285)
        self.assertEqual(metaphlan_result.taxa['d__Archaea'], 12)
        self.assertEqual(metaphlan_result.taxa['d__Bacteria|p__Proteobacteria'], 7285377)
        self.assertEqual(metaphlan_result.taxa['d__Archaea|p__Euryarchaeota|c__Methanomicrobia'], 2)
        self.assertEqual(metaphlan_result.taxa['d__Viruses|o__Caudovirales'], 1694)

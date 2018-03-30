"""Test suite for Microbe Directory tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.methyltransferases import MethylToolResult

from tests.base import BaseTestCase

from .factory import create_values


class TestMethylsModel(BaseTestCase):
    """Test suite for Microbe Directory tool result model."""

    def test_add_methyls(self):
        """Ensure Microbe Directory result model is created correctly."""

        methyls = MethylToolResult(**create_values())
        sample = Sample(name='SMPL_01',
                        align_to_methyltransferases=methyls).save()
        self.assertTrue(sample.align_to_methyltransferases)

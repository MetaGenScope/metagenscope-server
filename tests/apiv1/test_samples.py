"""Test suite for Sample module."""

import json

from tests.base import BaseTestCase
from tests.utils import add_sample


class TestSampleModule(BaseTestCase):
    """Tests for the Sample module."""

    def test_get_single_sample(self):
        """Ensure get single group behaves correctly."""
        sample = add_sample(name='SMPL_01')
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/{sample_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            sample = data['data']['sample']
            self.assertIn('SMPL_01', sample['name'])
            self.assertTrue('metadata' in sample)
            self.assertTrue('created_at' in sample)
            self.assertIn('success', data['status'])

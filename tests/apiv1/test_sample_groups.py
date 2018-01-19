"""Test suite for Sample Group module."""

import json

from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestSampleGroupModule(BaseTestCase):
    """Tests for the SampleGroup module."""

    def test_get_single_sample_groups(self):
        """Ensure get single group behaves correctly."""
        group = add_sample_group(name='Sample Group One')
        with self.client:
            response = self.client.get(
                f'/api/v1/sample_group/{group.id}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('Sample Group One', data['data']['name'])
            self.assertIn('public', data['data']['access_scheme'])
            self.assertIn('success', data['status'])

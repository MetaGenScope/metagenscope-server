"""Test suite for Sample Group module."""

import json

from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestSampleGroupModule(BaseTestCase):
    """Tests for the SampleGroup module."""

    def test_get_single_sample_groups(self):
        """Ensure get single group behaves correctly."""
        group = add_sample_group(name='Sample Group One')
        group_uuid = str(group.id)
        with self.client:
            response = self.client.get(
                f'/api/v1/sample_group/{group_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sample Group One', data['data']['sample_group']['name'])
            self.assertIn('public', data['data']['sample_group']['access_scheme'])
            self.assertTrue('created_at' in data['data']['sample_group'])
            self.assertIn('success', data['status'])

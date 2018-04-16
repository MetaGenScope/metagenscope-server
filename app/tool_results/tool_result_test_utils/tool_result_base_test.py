"""Base test suite and utilities for tool result modules."""

import json

from app.samples.sample_models import Sample

from tests.base import BaseTestCase
from tests.utils import add_sample, get_test_user


class BaseToolResultTest(BaseTestCase):
    """Test suite for VFDB tool result model."""

    def generic_add_test(self, result, tool_result_name):
        """Ensure tool result model is created correctly."""
        sample = Sample(name='SMPL_01',
                        **{tool_result_name: result}).save()
        self.assertTrue(getattr(sample, tool_result_name))

    def generic_test_upload(self, vals, tool_result_name):
        """Ensure a raw tool result can be uploaded."""
        auth_headers, _ = get_test_user(self.client)

        metadata = {'category_01': 'value_01'}
        sample = add_sample(name='SMPL_Microbe_Directory_01', metadata=metadata)
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/{tool_result_name}',
                headers=auth_headers,
                data=json.dumps(vals),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            for field in vals:
                self.assertIn(field, data['data'])

        # Reload object to ensure microbe directory result was stored properly
        sample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(getattr(sample, tool_result_name))

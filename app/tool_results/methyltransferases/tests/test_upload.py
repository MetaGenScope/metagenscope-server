"""Test suite for Methyl tool result uploads."""

import json

from app.samples.sample_models import Sample
from tests.base import BaseTestCase
from tests.utils import with_user

from .factory import create_values


class TestMethylsUploads(BaseTestCase):
    """Test suite for Methyl tool result uploads."""

    @with_user
    def test_upload_methyls(self, auth_headers, *_):
        """Ensure a raw Methyl tool result can be uploaded."""
        sample = Sample(name='SMPL_Microbe_Directory_01').save()
        sample_uuid = str(sample.uuid)
        vals = create_values()
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/align_to_methyltransferases',
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
        self.assertTrue(sample.align_to_methyltransferases)

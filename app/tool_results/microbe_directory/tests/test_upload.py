"""Test suite for Microbe Directory tool result uploads."""

import json

from app.samples.sample_models import Sample
from tests.base import BaseTestCase
from tests.utils import with_user

from .constants import TEST_DIRECTORY


class TestKrakenUploads(BaseTestCase):
    """Test suite for Microbe Directory tool result uploads."""

    @with_user
    def test_upload_microbe_directory(self, auth_headers, *_):
        """Ensure a raw Microbe Directory tool result can be uploaded."""
        sample = Sample(name='SMPL_Microbe_Directory_01').save()
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/microbe_directory_annotate',
                headers=auth_headers,
                data=json.dumps(TEST_DIRECTORY),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            for field in TEST_DIRECTORY:
                self.assertIn(field, data['data'])

        # Reload object to ensure microbe directory result was stored properly
        sample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(sample.microbe_directory_annotate)

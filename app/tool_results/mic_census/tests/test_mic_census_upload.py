"""Test suite for Microbe Census tool result uploads."""

import json

from app.api.utils import uuid2slug
from app.samples.sample_models import Sample
from app.tool_results.mic_census.tests.constants import TEST_CENSUS
from tests.base import BaseTestCase
from tests.utils import with_user


class TestMicCensusUploads(BaseTestCase):
    """Test suite for Microbe Census tool result uploads."""

    @with_user
    def test_upload_mic_census(self, auth_headers, *_):
        """Ensure a raw Microbe Census tool result can be uploaded."""
        sample = Sample(name='SMPL_MicCensus_01').save()
        sample_uuid = sample.uuid
        sample_slug = uuid2slug(sample_uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_slug}/mic_census',
                headers=auth_headers,
                data=json.dumps(TEST_CENSUS),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['data']['average_genome_size'], 3)
            self.assertEqual(data['data']['total_bases'], 5)
            self.assertEqual(data['data']['genome_equivalents'], 250)
            self.assertIn('success', data['status'])

        # Reload object to ensure HMP Sites result was stored properly
        sample = Sample.objects(uuid=sample_uuid)[0]
        self.assertTrue(sample.mic_census)

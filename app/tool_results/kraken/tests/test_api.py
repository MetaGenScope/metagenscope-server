"""Test suite for Kraken tool result uploads."""

import json

from app.samples.sample_models import Sample
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.kraken.tests.constants import TEST_TAXA
from tests.base import BaseTestCase
from tests.utils import with_user


KRAKEN_NAME = KrakenResultModule.name()


class TestKrakenUploads(BaseTestCase):
    """Test suite for Kraken tool result uploads."""

    @with_user
    def test_upload_kraken(self, auth_headers, *_):
        """Ensure a raw Kraken tool result can be uploaded."""
        sample = Sample(name='SMPL_Kraken_01').save()
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/{KRAKEN_NAME}',
                headers=auth_headers,
                data=json.dumps(dict(
                    taxa=TEST_TAXA,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('taxa', data['data'])
            self.assertEqual(data['data']['taxa']['d__Viruses'], 1733)
            self.assertIn('success', data['status'])

        # Reload object to ensure kraken result was stored properly
        sample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(hasattr(sample, KRAKEN_NAME))

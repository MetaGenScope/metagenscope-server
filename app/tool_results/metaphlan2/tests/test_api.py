"""Test suite for Metaphlan 2 tool result uploads."""

import json

from app.samples.sample_models import Sample
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.metaphlan2.tests.constants import TEST_TAXA
from tests.base import BaseTestCase
from tests.utils import with_user


METAPHLAN2_NAME = Metaphlan2ResultModule.name()


class TestMetaphlan2Uploads(BaseTestCase):
    """Test suite for Metaphlan 2 tool result uploads."""

    @with_user
    def test_upload_metaphlan2(self, auth_headers, *_):
        """Ensure a raw Metaphlan 2 tool result can be uploaded."""
        sample = Sample(name='SMPL_Metaphlan_01').save()
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/{METAPHLAN2_NAME}',
                headers=auth_headers,
                data=json.dumps(dict(
                    taxa=TEST_TAXA,
                )),
                content_type='application/json',
            )
            # Ensure response contains Metaphlan data
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('taxa', data['data'])
            self.assertEqual(data['data']['taxa']['d__Viruses'], 1733)
            self.assertIn('success', data['status'])

        # Reload object to ensure Metaphlan 2 result was stored properly
        sample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(hasattr(sample, METAPHLAN2_NAME))

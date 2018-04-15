"""Test suite for HMP Sites tool result uploads."""

import json

from app.samples.sample_models import Sample
from app.tool_results.hmp_sites.tests.constants import TEST_HMP
from app.tool_results.hmp_sites.constants import MODULE_NAME
from tests.base import BaseTestCase
from tests.utils import with_user


class TestHmpSitesUploads(BaseTestCase):
    """Test suite for HMP Sites tool result uploads."""

    @with_user
    def test_upload_hmp_sites(self, auth_headers, *_):
        """Ensure a raw HMP Sites tool result can be uploaded."""
        sample = Sample(name='SMPL_HMP_01').save()
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/hmp_site_dists',
                headers=auth_headers,
                data=json.dumps(TEST_HMP),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('gut', data['data'])
            self.assertIn('skin', data['data'])
            self.assertIn('throat', data['data'])
            self.assertIn('urogenital', data['data'])
            self.assertIn('airways', data['data'])
            self.assertEqual(data['data']['gut'], 0.6)
            self.assertIn('success', data['status'])

        # Reload object to ensure HMP Sites result was stored properly
        sample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(getattr(sample, MODULE_NAME))

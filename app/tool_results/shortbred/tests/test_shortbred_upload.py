"""Test suite for Shortbred tool result uploads."""

import json

from app.samples.sample_models import Sample
from app.tool_results.shortbred.tests.constants import TEST_ABUNDANCES
from tests.base import BaseTestCase
from tests.utils import with_user


class TestShortbredUploads(BaseTestCase):
    """Test suite for Shortbred tool result uploads."""

    @with_user
    def test_upload_shortbred(self, auth_headers, *_):
        """Ensure a raw Shortbred tool result can be uploaded."""
        sample = Sample(name='SMPL_Shortbred_01').save()
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/shortbred',
                headers=auth_headers,
                data=json.dumps(dict(
                    abundances=TEST_ABUNDANCES,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('abundances', data['data'])
            abundances = data['data']['abundances']
            self.assertEqual(abundances['AAA98484'], 3.996805816740154)
            self.assertEqual(abundances['BAC77251'], 3.6770613514009423)
            self.assertEqual(abundances['TEM_137'], 38.705908962115174)
            self.assertEqual(abundances['YP_002317674'], 4.178478808410161)
            self.assertEqual(abundances['YP_310429'], 10.943634974407566)
            self.assertEqual(abundances['soxR_2'], 5.10702965472353)
            self.assertIn('success', data['status'])

        # Reload object to ensure HMP Sites result was stored properly
        sample = Sample.objects(uuid=sample_uuid)[0]
        self.assertTrue(sample.shortbred)

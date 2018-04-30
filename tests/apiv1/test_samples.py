"""Test suite for Sample module."""

import json
from uuid import UUID, uuid4

from tests.base import BaseTestCase
from tests.utils import add_sample, add_sample_group, with_user


class TestSampleModule(BaseTestCase):
    """Tests for the Sample module."""

    @with_user
    def test_add_sample(self, auth_headers, *_):
        """Ensure a new sample can be added to the database."""
        sample_name = 'Exciting Research Starts Here'
        sample_group = add_sample_group(name='A Great Name')
        with self.client:
            response = self.client.post(
                f'/api/v1/samples',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=sample_name,
                    sample_group_uuid=str(sample_group.id),
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['sample'])
            self.assertEqual(sample_name, data['data']['sample']['name'])

        sample_uuid = UUID(data['data']['sample']['uuid'])
        self.assertIn(sample_uuid, sample_group.sample_ids)

    @with_user
    def test_add_sample_missing_group(self, auth_headers, *_):
        """Ensure adding a sample with an invalid group uuid fails."""
        sample_group_uuid = str(uuid4())
        with self.client:
            response = self.client.post(
                f'/api/v1/samples',
                headers=auth_headers,
                data=json.dumps(dict(
                    name='Exciting Research Starts Here',
                    sample_group_uuid=sample_group_uuid,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertEqual('Sample Group does not exist!', data['message'])

    def test_get_single_sample(self):
        """Ensure get single sample behaves correctly."""
        sample = add_sample(name='SMPL_01')
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/{sample_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            sample = data['data']['sample']
            self.assertIn('SMPL_01', sample['name'])
            self.assertIn('metadata', sample)
            self.assertIn('analysis_result_uuid', sample)
            self.assertIn('created_at', sample)

    def test_get_sample_uuid_from_name(self):
        """Ensure get sample uuid behaves correctly."""
        sample_name = 'SMPL_01'
        sample = add_sample(name=sample_name)
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/getid/{sample_name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(sample_uuid, data['data']['sample_uuid'])
            self.assertEqual(sample_name, data['data']['sample_name'])

    @with_user
    def test_kick_off_all_middleware(self, auth_headers, *_):  # pylint: disable=invalid-name
        """Ensure all middleware can be kicked off."""
        sample_group = self.prepare_middleware_test()

        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{str(sample_group.id)}/middleware',
                headers=auth_headers,
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 500)
            data_load = json.loads(response.data.decode())
            self.assertIn('failure', data_load['data'])
            self.assertIn('success', data_load['data'])
            self.assertIn('error', data_load['status'])
            self.assertEqual(len(data_load['data']['success']), 1)
            self.assertTrue(len(data_load['data']['failure']) > 0)

    @with_user
    def test_kick_off_single_middleware(self, auth_headers, *_):  # pylint: disable=invalid-name
        """Ensure single middleware can be kicked off."""
        sample_group = self.prepare_middleware_test()

        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{str(sample_group.id)}/middleware',
                headers=auth_headers,
                content_type='application/json',
                data=json.dumps(dict(
                    tools=['ancestry_summary'],
                )),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('failure', data['data'])
            self.assertIn('success', data['data'])
            self.assertEqual(len(data['data']['success']), 1)
            self.assertEqual(len(data['data']['failure']), 0)
            
            


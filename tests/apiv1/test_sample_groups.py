"""Test suite for Sample Group module."""

import json

from tests.base import BaseTestCase
from tests.utils import add_sample, add_sample_group, with_user


class TestSampleGroupModule(BaseTestCase):
    """Tests for the SampleGroup module."""

    @with_user
    def test_add_sample_group(self, auth_headers, *_):
        """Ensure a new sample group can be added to the database."""
        group_name = 'The Most Sampled of Groups'
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=group_name,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertEqual(group_name, data['data']['sample_group']['name'])

    @with_user
    def test_add_samples_to_group(self, auth_headers, *_):
        """Ensure samples can be added to a sample group."""
        sample_group = add_sample_group(name='A Great Name')
        sample = add_sample(name='SMPL_01')
        endpoint = f'/api/v1/sample_groups/{str(sample_group.id)}/samples'
        with self.client:
            response = self.client.post(
                endpoint,
                headers=auth_headers,
                data=json.dumps(dict(
                    sample_uuids=[str(sample.uuid)],
                )),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertIn('success', data['status'])
            self.assertIn(sample.uuid, sample_group.sample_ids)

    @with_user
    def test_add_duplicate_sample_group(self, auth_headers, *_):
        """Ensure failure for non-unique Sample Group name."""
        group_name = 'The Most Sampled of Groups'
        add_sample_group(name=group_name)
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=group_name,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertEqual('Sample Group with that name already exists.', data['message'])

    def test_get_single_sample_groups(self):
        """Ensure get single group behaves correctly."""
        group = add_sample_group(name='Sample Group One')
        group_uuid = str(group.id)
        with self.client:
            response = self.client.get(
                f'/api/v1/sample_groups/{group_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sample Group One', data['data']['sample_group']['name'])
            self.assertIn('public', data['data']['sample_group']['access_scheme'])
            self.assertTrue('created_at' in data['data']['sample_group'])
            self.assertIn('success', data['status'])

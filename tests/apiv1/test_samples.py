"""Test suite for Sample module."""

import json

# from app.sample_groups.sample_group_models import SampleGroup

from tests.base import BaseTestCase
from tests.utils import add_sample, add_sample_group, with_user


class TestSampleModule(BaseTestCase):
    """Tests for the Sample module."""

    @with_user
    def test_add_sample(self, auth_headers, *_):
        """Ensure a new sample can be added to the database."""
        sample_name = 'Exciting Research Starts Here'
        sample_group = add_sample_group(name='A Great Name')
        sample_group_uuid = str(sample_group.id)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=sample_name,
                    sample_group_uuid=sample_group_uuid,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['sample'])
            self.assertEqual(sample_name, data['data']['sample']['name'])

        # Reload sample group
        # sample_group = SampleGroup.query.filter_by(id=sample_group.id).one()
        sample_uuid = data['data']['sample']['uuid']
        self.assertIn(sample_uuid, sample_group.sample_ids)

    def test_get_single_sample(self):
        """Ensure get single group behaves correctly."""
        sample = add_sample(name='SMPL_01')
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/{sample_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            sample = data['data']['sample']
            self.assertIn('SMPL_01', sample['name'])
            self.assertTrue('metadata' in sample)
            self.assertTrue('created_at' in sample)
            self.assertIn('success', data['status'])

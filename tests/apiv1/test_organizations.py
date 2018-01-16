"""Test suite for Organization module."""

import json

from uuid import uuid4

from app import db
from app.users.user_helpers import uuid2slug
from tests.base import BaseTestCase
from tests.utils import add_user, add_organization, with_user


class TestOrganizationService(BaseTestCase):
    """Tests for the Organizations Service."""

    @with_user
    def test_add_organization(self, auth_headers, *_):
        """Ensure a new organization can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=auth_headers,
                data=json.dumps(dict(
                    name='MetaGenScope',
                    adminEmail='admin@metagenscope.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('MetaGenScope was added!', data['message'])
            self.assertIn('success', data['status'])

    # pylint: disable=invalid-name
    @with_user
    def test_add_organization_invalid_json(self, auth_headers, *_):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=auth_headers,
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    # pylint: disable=invalid-name
    @with_user
    def test_add_organization_invalid_json_keys(self, auth_headers, *_):
        """Ensure error is thrown if the JSON object does not have a name key."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=auth_headers,
                data=json.dumps(dict(adminEmail='admin@metagenscope.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_invalid_token(self):
        """Ensure create organization route fails for invalid token."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=dict(Authorization='Bearer invalid'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_single_organization(self):
        """Ensure get single organization behaves correctly."""
        organization = add_organization('Test Organization', 'admin@test.org')
        slug = uuid2slug(str(organization.id))
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{slug}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('Test Organization', data['data']['name'])
            self.assertIn('admin@test.org', data['data']['admin_email'])
            self.assertIn('success', data['status'])

    def test_single_organization_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/blah',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Organization does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_organization_users(self):
        """Ensure getting users for an organization behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        organization = add_organization('Test Organization', 'admin@test.org')
        organization.users = [user]
        db.session.commit()

        slug = uuid2slug(str(organization.id))
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{slug}/users',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']['users']) == 1)
            self.assertTrue('username' in data['data']['users'][0])
            self.assertTrue('email' in data['data']['users'][0])
            self.assertIn('success', data['status'])

    def test_single_organization_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        randomSlug = uuid2slug(str(uuid4()))
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{randomSlug}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Organization does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_organizations(self):
        """Ensure get all organizations behaves correctly."""
        add_organization('Test Organization', 'admin@test.org')
        add_organization('Test Organization Two', 'admin@test.org')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['organizations']), 2)
            self.assertTrue('created_at' in data['data']['organizations'][0])
            self.assertTrue('created_at' in data['data']['organizations'][1])
            self.assertIn('Test Organization', data['data']['organizations'][0]['name'])
            self.assertIn(
                'admin@test.org', data['data']['organizations'][0]['admin_email'])
            self.assertIn('Test Organization Two', data['data']['organizations'][1]['name'])
            self.assertIn(
                'admin@test.org', data['data']['organizations'][1]['admin_email'])
            self.assertIn('success', data['status'])

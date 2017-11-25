"""Test suite for Organization service"""

import json

from app.tests.base import BaseTestCase
from app.tests.utils import add_user


class TestOrganizationService(BaseTestCase):
    """Tests for the Organizations Service."""

    def test_add_organization(self):
        """Ensure a new organization can be added to the database."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/organizations',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
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
    def test_add_organization_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/organizations',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    # pylint: disable=invalid-name
    def test_add_organization_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a name key."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/organizations',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
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
                '/organizations',
                headers=dict(Authorization='Bearer invalid'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

"""Test suite for the authorization endpoints."""

# pylint: disable=invalid-name

import json
import time

from app.extensions import db
from app.users.UserModels import User
from tests.base import BaseTestCase
from tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    """Test suite for the authorization endpoints."""

    def test_user_registration(self):
        """Test user registration."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='justatest',
                    email='test@test.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        """Ensure registration fails with duplicate email address."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='michael',
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_duplicate_username(self):
        """Ensure registration fails with duplicate email username."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='test',
                    email='test@test.com2',
                    password='test'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json(self):
        """Ensure registration fails for invalid JSON payload."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        """Ensure registration fails for JSON payload missing username key."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        """Ensure registration fails for JSON payload missing email key."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='justatest', password='test')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        """Ensure registration fails for JSON payload missing password key."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='justatest', email='test@test.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_registered_user_login(self):
        """Ensure login works for registered user."""
        with self.client:
            add_user('test', 'test@test.com', 'test')
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        """Ensure login fails without a registered user."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        """Ensure client can log out."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            # User login
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            # Valid token logout
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        """Ensure logout fails for expired token."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            # invalid token logout
            time.sleep(4)
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        """Ensure logout fails for invalid token."""
        with self.client:
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=dict(Authorization='Bearer invalid'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        """Ensure user status route works."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertTrue(data['data']['email'] == 'test@test.com')
            self.assertTrue(data['data']['active'] is True)
            self.assertTrue(data['data']['created_at'])
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        """Ensure user status route fails for invalid request."""
        with self.client:
            response = self.client.get(
                '/api/v1/auth/status',
                headers=dict(Authorization='Bearer invalid'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        """Ensure logout fails for inactive user."""
        add_user('test', 'test@test.com', 'test')
        # Update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_status_inactive(self):
        """Ensure user session fails for inactive user."""
        add_user('test', 'test@test.com', 'test')
        # Update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/api/v1/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')
            self.assertEqual(response.status_code, 401)

"""Test suite for Ping service."""

import json

from app.tests.base import BaseTestCase


class TestPingService(BaseTestCase):
    """Tests for the Users Service."""

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/api/v1/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

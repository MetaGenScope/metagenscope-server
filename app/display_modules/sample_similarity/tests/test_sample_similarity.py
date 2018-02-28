"""Test suite for Sample Similarity result type."""

import json

from tests.base import BaseTestCase
from tests.factories.query_result import QueryResultMetaFactory


class TestSampleSimilarityModule(BaseTestCase):
    """Tests for the Sample Similarity module."""

    def test_get_sample_similarity(self):
        """Ensure getting a single sample similarity behaves correctly."""

        query_result = QueryResultMetaFactory(processed=True)
        with self.client:
            response = self.client.get(
                f'/api/v1/query_results/{query_result.id}/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'S')
            self.assertIn('data', data['data'])
            sample_similarity = data['data']['data']
            self.assertIn('categories', sample_similarity)
            self.assertIn('tools', sample_similarity)
            self.assertIn('data_records', sample_similarity)
            self.assertTrue(len(sample_similarity['data_records']) > 0)
            self.assertIn('SampleID', sample_similarity['data_records'][0])

    # pylint: disable=invalid-name
    def test_get_pending_sample_similarity(self):
        """Ensure getting a pending single sample similarity behaves correctly."""

        query_result = QueryResultMetaFactory()
        with self.client:
            response = self.client.get(
                f'/api/v1/query_results/{query_result.id}/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Query Result has not finished processing.', data['message'])
            self.assertIn('fail', data['status'])

    # pylint: disable=invalid-name
    def test_get_malformed_id_sample_similarity(self):
        """Ensure getting a malformed ID for a single sample similarity behaves correctly."""

        with self.client:
            response = self.client.get(
                f'/api/v1/query_results/foobarblah/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            message = ('\'foobarblah\' is not a valid ObjectId, '
                       'it must be a 12-byte input or a 24-character hex string')
            self.assertIn(message, data['message'])
            self.assertIn('fail', data['status'])

    # pylint: disable=invalid-name
    def test_get_missing_sample_similarity(self):
        """Ensure getting a missing single sample similarity behaves correctly."""

        with self.client:
            response = self.client.get(
                f'/api/v1/query_results/abcdefabcdefabcdefabcdef/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Query Result does not exist.', data['message'])
            self.assertIn('fail', data['status'])

"""Test suite for Reads Classified model."""

from mongoengine import ValidationError

from app.query_results.query_result_models import (
    QueryResultMeta,
    ReadsClassifiedResult,
    ReadsClassifiedResultWrapper,
)
from tests.base import BaseTestCase


class TestReadsClassifiedResult(BaseTestCase):
    """Test suite for Taxon Abundance model."""

    def test_add_reads_classified(self):
        """Ensure Reads Classified model is created correctly."""
        categories = ['human', 'bacteria']
        sample_names = ['D02', 'G04']
        data = [
            {
                'category': 'human',
                'values': [91.68918236362886, 89.56049654224611],
            },
            {
                'category': 'bacteria',
                'values': [0.6247009170848492, 0.9150549547549014],
            },
        ]

        reads_classified = ReadsClassifiedResult(categories=categories,
                                                 sample_names=sample_names,
                                                 data=data)
        wrapper = ReadsClassifiedResultWrapper(data=reads_classified)
        result = QueryResultMeta(reads_classified=wrapper).save()
        self.assertTrue(result.id)
        self.assertTrue(result.reads_classified)

    def test_add_missing_category(self):
        """Ensure saving model fails if data contains unknown category."""
        categories = ['human']
        sample_names = ['D02', 'G04']
        data = [
            {
                'category': 'human',
                'values': [91.68918236362886, 89.56049654224611],
            },
            {
                'category': 'bacteria',
                'values': [0.6247009170848492, 0.9150549547549014],
            },
        ]

        reads_classified = ReadsClassifiedResult(categories=categories,
                                                 sample_names=sample_names,
                                                 data=data)
        wrapper = ReadsClassifiedResultWrapper(data=reads_classified)
        result = QueryResultMeta(reads_classified=wrapper)
        self.assertRaises(ValidationError, result.save)

    def test_add_value_count_mismatch(self):
        """Ensure saving model fails for mismatched value count."""
        categories = ['human']
        sample_names = ['D02']
        data = [
            {
                'category': 'human',
                'values': [91.68918236362886, 89.56049654224611],
            },
        ]

        reads_classified = ReadsClassifiedResult(categories=categories,
                                                 sample_names=sample_names,
                                                 data=data)
        wrapper = ReadsClassifiedResultWrapper(data=reads_classified)
        result = QueryResultMeta(reads_classified=wrapper)
        self.assertRaises(ValidationError, result.save)

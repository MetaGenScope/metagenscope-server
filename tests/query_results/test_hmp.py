"""Test suite for HMP model."""

import copy

from mongoengine import ValidationError

from app.query_results.query_result_models import QueryResultMeta
from app.api.v1.display_modules.hmp_module import (
    HMPResult,
    HMPModule,
)
from tests.base import BaseTestCase


# Define aliases
HMPResultWrapper = HMPModule.get_query_result_wrapper()


# Test data
# pylint: disable=invalid-name
categories = {
    'front-phone': ['glass', 'plastic'],
}
sites = ['airways', 'skin']
data = {
    'front-phone': [
        {
            'name': 'glass',
            'data': [
                [
                    0.006239664503752573,
                    0.24653229840348845,
                    0.5481507432007606,
                    0.8753560450650528,
                    0.9941735059896694,
                ],
                [
                    0.028727401965407018,
                    0.26434785073550915,
                    0.5979009767718476,
                    0.8882099591978124,
                    0.9990592666450798,
                ],
            ],
        },
        {
            'name': 'plastic',
            'data': [
                [
                    0.0023008752218525164,
                    0.04951944574662548,
                    0.35616849987092186,
                    0.5307249849949371,
                    0.9810864819930054,
                ],
                [
                    0.005473498255927245,
                    0.221135010703977,
                    0.4248223065732196,
                    0.6773667403470901,
                    0.9875887290501434,
                ],
            ],
        },
    ],
}
# pylint: enable=invalid-name


class TestHMPResult(BaseTestCase):
    """Test suite for HMP model."""

    def test_add_hmp(self):
        """Ensure HMP model is created correctly."""
        hmp = HMPResult(categories=categories, sites=sites, data=data)
        wrapper = HMPResultWrapper(data=hmp)
        result = QueryResultMeta(hmp=wrapper).save()
        self.assertTrue(result.id)
        self.assertTrue(result.hmp)

    def test_add_missing_category(self):
        """Ensure saving model fails if category is missing from `data`."""
        hmp = HMPResult(categories=categories, sites=sites, data={})
        wrapper = HMPResultWrapper(data=hmp)
        result = QueryResultMeta(hmp=wrapper)
        self.assertRaises(ValidationError, result.save)

    def test_add_missing_category_value(self):
        """Ensure saving model fails if category value is missing from `data`."""
        incomplete_data = copy.deepcopy(data)
        incomplete_data['front-phone'] = incomplete_data['front-phone'][:1]
        hmp = HMPResult(categories=categories, sites=sites, data=incomplete_data)
        wrapper = HMPResultWrapper(data=hmp)
        result = QueryResultMeta(hmp=wrapper)
        self.assertRaises(ValidationError, result.save)

    def test_add_missing_site(self):
        """Ensure saving model fails if site is missing from `data`."""
        incomplete_data = copy.deepcopy(data)
        incomplete_data['front-phone'][0]['data'] = incomplete_data['front-phone'][0]['data'][:1]
        hmp = HMPResult(categories=categories, sites=sites, data=incomplete_data)
        wrapper = HMPResultWrapper(data=hmp)
        result = QueryResultMeta(hmp=wrapper)
        self.assertRaises(ValidationError, result.save)

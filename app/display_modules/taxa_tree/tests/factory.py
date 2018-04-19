# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating ReadStats models for testing."""

import factory
from random import random, randint

from app.display_modules.taxa_tree import TaxaTreeResult
from app.tool_results.read_stats.tests.factory import create_values


def generate_random_tree(parent=None, level=0, parent_size=100):
    name = 'level_{}'.format(level)
    size = random() * parent_size
    parent_name = parent.split('|')[-1]
    if parent is None:
        parent_name = None
        name = 'root'
        parent_size = 100
    node = {
        'name': name,
        'size': size,
        'parent': parent_name,
        'children': [
            generate_random_tree(
                parent=parent + '|' + name,
                level=level + 1,
                parent_size=size,
            )
            for _ in randint(3, 6)
        ]
    }
    if random() < 0.5:
        node['children'] = []
    return node


class TaxaTreeFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for TaxaTree's Read Stats."""

    class Meta:
        """Factory metadata."""

        model = TaxaTreeResult

    @factory.lazy_attribute
    def metaphlan2(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        return generate_random_tree()

    @factory.lazy_attribute
    def kraken(self):  # pylint: disable=no-self-use
        """Generate random kraken."""
        return generate_random_tree()

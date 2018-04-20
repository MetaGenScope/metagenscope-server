# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Taxa Tree models for testing."""

from random import random, randint
import factory

from app.display_modules.taxa_tree import TaxaTreeResult


def generate_random_tree(parent=None, level=0, parent_size=100):
    """Return a random, plausible, taxa tree."""
    if parent is None:
        parent_name = None
        name = 'root'
        parent_size = 100
    else:
        name = 'level_{}'.format(level)
        size = random() * parent_size
        parent_name = parent.split('|')[-1]

    children = []
    if random() < (1 / (level + 1)):
        children = [
            generate_random_tree(
                parent=parent + '|' + name,
                level=level + 1,
                parent_size=size,
            )
            for _ in randint(3, 6)
        ]

    return {
        'name': name,
        'size': size,
        'parent': parent_name,
        'children': children
    }


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

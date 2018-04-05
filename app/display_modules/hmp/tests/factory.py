# pylint: disable=missing-docstring,too-few-public-methods,no-self-use

"""Factory for generating HMP models for testing."""

from random import random, randint

import factory

from app.display_modules.hmp import HMPResult


def fake_distribution():
    """Return a random 'distribution'."""
    distro = [random() for _ in range(5)]
    return sorted(distro)


def fake_categories():
    """Return fake categories."""
    out = {}
    for cat_name in ['cat_1', 'cat_2']:
        out[cat_name] = []
        for i in range(randint(2, 4)):
            out[cat_name].append(cat_name + str(i))
    return out


def fake_sites():
    """Return fake sites."""
    return ['skin', 'oral', 'urogenital', 'airways']


class HMPFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's HMP."""

    class Meta:
        """Factory metadata."""

        model = HMPResult

    @factory.lazy_attribute
    def categories(self):
        """Return categories."""
        return fake_categories()

    @factory.lazy_attribute
    def sites(self):
        """Return body sites."""
        return fake_sites()

    @factory.lazy_attribute
    def data(self):
        """Return plausible data."""
        out = {}
        for cat_vals in self.categories.values():
            for cat_val in cat_vals:
                out[cat_val] = [{'name': site, 'data': fake_distribution()}
                                for site in self.sites]
        return out

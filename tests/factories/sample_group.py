# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Sample Group models for testing."""

import factory

from app import db
from app.sample_groups.sample_group_models import SampleGroup


class SampleGroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Sample Group."""

    class Meta:
        model = SampleGroup
        session = db.session

    name = factory.Faker('city')
    access_scheme = 'public'

# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Read Classified models for testing."""

import factory
from app.display_modules.reads_classified import ReadsClassifiedResult
from app.tool_results.reads_classified.tests.factory import create_values


class ReadsClassifiedFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Read Stats."""

    class Meta:
        """Factory metadata."""

        model = ReadsClassifiedResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_values()
        return samples

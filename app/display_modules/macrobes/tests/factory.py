# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Macrobe models for testing."""

import factory

from app.display_modules.macrobes import MacrobeResult
from app.tool_results.macrobes.tests.factory import create_values


class MacrobeFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Macrobe."""

    class Meta:
        """Factory metadata."""

        model = MacrobeResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_values()['macrobes']['rpkm']
        return samples

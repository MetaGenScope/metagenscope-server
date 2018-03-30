# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

import factory

from app.display_modules.methyls import MethylResult


def create_one_sample():
    """Return an example sa,ple for MethylResult."""
    return {
        'rpkm': {'sample_gene_1': 2.5, 'sample_gene_2': 3.5},
        'rpkmg': {'sample_gene_1': 5.5, 'sample_gene_2': 4.5},
    }


class MethylsFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    class Meta:
        """Factory metadata."""

        model = MethylResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_one_sample()
        return samples

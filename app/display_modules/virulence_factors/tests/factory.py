# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

import factory

from app.display_modules.virulence_factors import VFDBResult


def create_one_sample():
    """Return an example sample for VFDBResult."""
    return {
        'rpkm': {'vfdb_sample_gene_1': 2.1, 'vfdb_sample_gene_2': 3.5},
        'rpkmg': {'vfdb_sample_gene_1': 5.1, 'vfdb_sample_gene_2': 4.5},
    }


class VFDBFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    class Meta:
        """Factory metadata."""

        model = VFDBResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample_{i}'] = create_one_sample()
        return samples

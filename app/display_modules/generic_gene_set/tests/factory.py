# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

import factory


def create_one_sample():
    """Return an example sample for VFDBResult."""
    return {
        'rpkm': {'sample_gene_1': 2.1, 'sample_gene_2': 3.5},
        'rpkmg': {'sample_gene_1': 5.1, 'sample_gene_2': 4.5},
    }


class GeneSetFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample_{i}'] = create_one_sample()
        return samples

# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Query Result models for testing."""

import random

import factory

from app.query_results.query_result_models import ToolDocument, SampleSimilarityResult, QueryResult


class ToolFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Query Result's Sample Similarity's tool."""
    class Meta:
        model = ToolDocument

    x_label = factory.Faker('word').generate({})
    y_label = factory.Faker('word').generate({})


class SampleSimilarityFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Query Result's Sample Similarity."""
    class Meta:
        model = SampleSimilarityResult

    @factory.lazy_attribute
    # pylint: disable=no-self-use
    def categories(self):
        category_name = factory.Faker('word').generate({})
        return {category_name: factory.Faker('words', nb=4).generate({})}

    @factory.lazy_attribute
    # pylint: disable=no-self-use
    def tools(self):
        tool_name = factory.Faker('word').generate({})
        return {tool_name: ToolFactory()}

    @factory.lazy_attribute
    def data_records(self):
        name = factory.Faker('company').generate({}).replace(' ', '_')
        def record(i):
            result = {'SampleID': f'{name}__seq{i}'}
            for category, category_values in self.categories.items():
                result[category] = random.choice(category_values)

            decimal = factory.Faker('pyfloat', left_digits=0, positive=True)
            for tool in self.tools:
                result[f'{tool}_x'] = decimal.generate({})
                result[f'{tool}_y'] = decimal.generate({})

            return result

        return [record(i) for i in range(20)]


class QueryResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Query Result."""

    class Meta:
        model = QueryResult

    status = 'P'
    sample_group_id = None
    sample_similarity = None

    class Params:
        processed = factory.Trait(
            status='S',
            sample_similarity=factory.SubFactory(SampleSimilarityFactory)
        )

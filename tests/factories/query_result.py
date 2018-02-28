# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Query Result models for testing."""

import random

import factory

from app.display_modules.sample_similarity import (
    ToolDocument,
    SampleSimilarityResult,
    SampleSimilarityDisplayModule,
)
from app.query_results.query_result_models import QueryResultMeta

# Define aliases
SampleSimilarityResultWrapper = SampleSimilarityDisplayModule.get_query_result_wrapper()


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

class SampleSimilarityWrapperFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Query Result's Sample Similarity status wrapper."""
    class Meta:
        model = SampleSimilarityResultWrapper

    status = 'P'
    data = None

    class Params:
        processed = factory.Trait(
            status='S',
            data=factory.SubFactory(SampleSimilarityFactory)
        )


class QueryResultMetaFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Query Result meta."""

    class Meta:
        model = QueryResultMeta

    sample_group_id = None
    sample_similarity = factory.SubFactory(SampleSimilarityWrapperFactory)

    class Params:
        processed = factory.Trait(
            sample_similarity=factory.SubFactory(SampleSimilarityWrapperFactory, processed=True)
        )

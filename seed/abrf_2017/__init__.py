"""MetaGenScope seed data from ARBF 2017."""

import json
import os

from app.query_results.query_result_models import SampleSimilarityResult


LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))


def load_sample_similarity():
    """Load Sample Similarity source JSON."""
    filename = os.path.join(LOCATION, 'sample-similarity_scatter.json')
    with open(filename, 'r') as f:
        datastore = json.load(f)['payload']
        result = SampleSimilarityResult(categories=datastore['categories'],
                                        tools=datastore['tools'],
                                        data_records=datastore['data_records'])
        return result

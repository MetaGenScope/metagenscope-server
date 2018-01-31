"""MetaGenScope seed data from ARBF 2017."""

import json
import os

from app.query_results.query_result_models import (
    SampleSimilarityResult,
    TaxonAbundanceResult,
    ReadsClassifiedResult,
    HMPResult
)


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


def load_taxon_abundance():
    """Load Taxon Abundance source JSON."""
    def transform_node(node):
        """Transform JSON node to expected type."""
        return {
            'id': node['id'],
            'name': node['nodeName'],
            'value': node['nodeValue']
        }

    filename = os.path.join(LOCATION, 'taxaflow.json')
    with open(filename, 'r') as f:
        datastore = json.load(f)['payload']['metaphlan2']
        nodes = [item for sublist in datastore['times'] for item in sublist]
        nodes = [transform_node(node) for node in nodes]
        result = TaxonAbundanceResult(nodes=nodes,
                                      edges=datastore['links'])
        return result


def load_reads_classified():
    """Load Reads Classified source JSON."""
    def transform_datum(datum):
        """Transform JSON datum to expected type."""
        return {'category': datum['name'], 'values': datum['data']}

    filename = os.path.join(LOCATION, 'reads-classified_col.json')
    with open(filename, 'r') as f:
        datastore = json.load(f)['payload']
        categories = datastore['categories']
        sample_names = datastore['samples']
        data = [transform_datum(datum) for datum in datastore['main']]
        result = ReadsClassifiedResult(categories=categories,
                                       sample_names=sample_names,
                                       data=data)
        return result


def load_hmp():
    """Load HMP source JSON."""
    filename = os.path.join(LOCATION, 'hmp_box.json')
    with open(filename, 'r') as f:
        datastore = json.load(f)['payload']
        categories = datastore['cats2vals']
        sites = datastore['sites']
        data = {category: datastore[category] for category in categories}
        result = HMPResult(categories=categories,
                           sites=sites,
                           data=data)
        return result

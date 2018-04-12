"""Handle loading data from JSON files."""

import json
import os

from app.display_modules.reads_classified import ReadsClassifiedResult


LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))


def load_reads_classified():
    """Load Reads Classified source JSON."""
    filename = os.path.join(LOCATION, 'reads-classified.json')
    with open(filename, 'r') as source:
        datastore = json.load(source)
        categories = datastore['categories']
        sample_names = ['UW_Madison_00']
        data = [{'category': category, 'values': [datastore['data'][index]]}
                for index, category in enumerate(categories)]
        result = ReadsClassifiedResult(categories=categories,
                                       sample_names=sample_names,
                                       data=data)
        return result

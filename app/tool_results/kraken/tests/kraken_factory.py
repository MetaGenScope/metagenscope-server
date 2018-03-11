"""Factory for generating Kraken result models for testing."""

import random

from app.tool_results.kraken import KrakenResult

DOMAINS = ['archaea', 'bacteria', 'eukarya']
KINGDOMS = ['archaebacteria', 'eubacteria', 'protista', 'fungi',
            'plantae', 'animalia']
PHYLA = ['acanthocephala', 'annelida', 'arthropoda', 'brachiopoda', 'bryozoa',
         'chaetognatha', 'chordata', 'cnidaria', 'ctenophora', 'cycliophora',
         'echinodermata', 'entoprocta', 'gastrotricha', 'gnathostomulida',
         'hemichordata', 'kinorhyncha', 'loricifera', 'micrognathozoa',
         'mollusca', 'nematoda', 'nematomorpha', 'nemertea', 'onychophora',
         'orthonectida', 'phoronida', 'placozoa', 'platyhelminthes',
         'porifera', 'priapulida', 'rhombozoa', 'rotifera', 'sipuncula',
         'tardigrada', 'xenacoelomorpha']


def create_kraken(taxa_count=10):
    """Create KrakenResult with specified number of taxa."""
    taxa = {}
    while len(taxa) < taxa_count:
        depth = random.randint(1, 3)
        entry = f'd_{random.choices(DOMAINS)[0]}'
        if depth >= 2:
            entry = f'{entry}|k_{random.choices(KINGDOMS)[0]}'
        if depth >= 3:
            entry = f'{entry}|p_{random.choices(PHYLA)[0]}'
        taxa[entry] = random.randint(0, 8e07)

    return KrakenResult(taxa=taxa)

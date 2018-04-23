"""Tasks to process Taxon Abundance results."""

import pandas as pd

from app.extensions import celery
from app.display_modules.utils import persist_result_helper
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.kraken import KrakenResultModule

from .models import TaxonAbundanceResult


def get_ranks(*tkns):
    """Return a rank code from a taxon ID."""
    out = []
    for tkn in tkns:
        rank = tkn.strip()[0].lower()
        if rank == 'd':
            rank = 'k'
        assert rank in 'kpcofgs'
        out.append(rank)
    return out


def node(tbl, key, name, value):
    """Update the node table."""
    try:
        tbl[key]['value'] += value
    except KeyError:
        display_name = name
        if '__' in display_name:
            display_name = display_name.split('__')[1]
        tbl[key] = {
            'id': name,
            'nodeName': display_name,
            'nodeValue': 100,
        }


def link(tbl, key, source, target, value):
    """Update the link table."""
    try:
        tbl[key]['value'] += value
    except KeyError:
        tbl[key] = {
            'source': source,
            'target': target,
            'value': value,
        }


def handle_one_taxon(nodes, links, sample_name, taxon, abundance):
    """Process a single taxon line."""
    taxa_tkns = taxon.split('|')
    for prev_taxa, cur_taxa in zip([None] + taxa_tkns[:-1], taxa_tkns):
        node_set = nodes['k']
        if prev_taxa:
            cur_rank = get_ranks(cur_taxa)
            node_set = nodes[cur_rank]

        if cur_taxa == taxa_tkns[-1]:
            node(node_set, cur_taxa, cur_taxa, abundance)
            if cur_rank == 's':
                link(links, cur_taxa + sample_name, cur_taxa, sample_name, abundance)

        if cur_taxa != taxa_tkns[0]:
            link(links, prev_taxa + cur_taxa, prev_taxa, cur_taxa, abundance)


def make_flow(taxa_vecs, min_abundance=0.05):
    """Return a JSON flow object.

    Takes a dict of sample_name to normalized taxa vectors
    """
    links = {}
    nodes = {
        'samples': {},
        'k': {}, 'p': {}, 'c': {}, 'o': {}, 'f': {}, 'g': {}, 's': {},
    }
    for sample_name, taxa_vec in taxa_vecs.items():
        node(nodes['samples'], sample_name, sample_name, 100)
        for taxon, abundance in taxa_vec.items():
            if (abundance < min_abundance) or 't__' in taxon:
                continue
            handle_one_taxon(nodes, links, sample_name, taxon, abundance)

        return {
            'nodes': [el for el in nodes.values()],
            'edges': links.values()
        }


def make_taxa_table(samples, tool_name):
    """Return a scaled taxa table."""
    taxa_tbl = {}
    for sample in samples:
        try:
            taxa_tbl[sample['name']] = sample[tool_name]['taxa']
        except KeyError:
            pass

    taxa_tbl = pd.DataFrame.from_dict(taxa_tbl, orient='index')
    taxa_tbl = taxa_tbl.apply(lambda col: col / col.sum(), axis=0)

    return taxa_tbl


@celery.task()
def make_all_flows(samples):
    """Determine flows by tool."""
    flow_tbl = {}
    tool_names = [Metaphlan2ResultModule.name(), KrakenResultModule.name()]
    for tool_name in tool_names:
        taxa_tbl = make_taxa_table(samples, tool_name)
        flow_tbl[tool_name] = make_flow(taxa_tbl)
    return flow_tbl


@celery.task(name='taxon_abundance.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Taxon results."""
    result = TaxonAbundanceResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)

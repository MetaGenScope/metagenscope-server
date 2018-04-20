"""Tasks for TaxaTree Wrangler."""

from app.extensions import celery
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.kraken import KrakenResultModule

from .models import TaxaTreeResult


@celery.task()
def taxa_tree_reducer(args):
    """Wrap collated samples as actual Result type."""
    return TaxaTreeResult(**args)


def get_total(taxa_list, delim):
    """Return the total abundance in the taxa list.

    This is not the sum b/c taxa lists are trees, implicitly.
    """
    total = 0
    for taxon, abund in taxa_list.items():
        tkns = taxon.split(delim)
        if len(tkns) == 1:
            total += abund
    return total


def convert_children_to_list(taxa_tree):
    """Convert a dictionary of children to a list, recursively."""
    children = taxa_tree['children']
    taxa_tree['children'] = [convert_children_to_list(child)
                             for child in children.values()]
    return taxa_tree


def get_taxa_tokens(taxon, delim, tkn_delim='__'):
    """Return a list of cleaned tokens."""
    tkns = taxon.split(delim)
    tkns = [tkn.split(tkn_delim)[-1] for tkn in tkns]
    return tkns


def recurse_tree(tree, tkns, i, leaf_size):
    """Return a recursively built tree."""
    is_leaf = (i + 1) == len(tkns)
    tkn = tkns[i]

    try:
        tree['children'][tkn]
    except KeyError:
        tree['children'][tkn] = {
            'name': tkn,
            'parent': 'root',
            'size': -1,
            'children': {},
        }
        if i > 0:
            tree['children'][tkn]['parent'] = tkns[i - 1]
        if is_leaf:
            tree['children'][tkn]['size'] = leaf_size
    if i != 0:
        assert tree['children'][tkn]['parent'] != 'root', '{} : {}'.format(tkn, tkns)
    if is_leaf:
        return tree['children'][tkn]
    return recurse_tree(tree, tkns, i + 1, leaf_size)


def reduce_taxa_list(taxa_list, delim='|'):
    """Return a tree built from a taxa list."""
    factor = 100 / get_total(taxa_list, delim)
    taxa_tree = {
        'name': 'root',
        'parent': None,
        'size': 100,
        'children': {}
    }
    for taxon, abund in taxa_list.items():
        tkns = get_taxa_tokens(taxon, delim)
        recurse_tree(taxa_tree, tkns, 0, factor * abund)
    taxa_tree = convert_children_to_list(taxa_tree)
    return taxa_tree


@celery.task()
def trees_from_sample(sample):
    """Build taxa trees for a given sample."""
    metaphlan2 = getattr(sample, Metaphlan2ResultModule.name())
    metaphlan2 = reduce_taxa_list(metaphlan2.taxa)
    kraken = getattr(sample, KrakenResultModule.name())
    kraken = reduce_taxa_list(kraken.taxa)
    return {
        'kraken': kraken,
        'metaphlan2': metaphlan2,
    }

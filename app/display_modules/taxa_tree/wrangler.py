"""Taxa Tree wrangler and related."""

from celery import chain

from app.extensions import celery
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result, collate_samples
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.read_stats import ReadStatsToolResultModule

from .constants import MODULE_NAME
from .models import TaxaTreeResult


@celery.task()
def read_stats_reducer(samples):
    """Wrap collated samples as actual Result type."""
    return ReadStatsResult(samples=samples)


def get_total(taxa_list, delim):
    total = 0
    for taxon, abund in taxa_list.items():
        tkns = taxon.split(delim)
        if len(tkns) == 1:
            total += abund
    return total


def convert_children_to_list(taxa_tree):
    children = taxa_tree['children']
    taxa_tree['children'] = [convert_children_to_list(child)
                             for child in children.values()]
    return taxa_tree


def recurse_tree(tree, tkns, i, leaf_size):
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

    if is_leaf:
        return tree['children'][tkn]
    else:
        return recurse_tree(tree, tkns, i + 1, leaf_size)


def reduce_taxa_list(taxa_list, delim='|'):
    factor = 100 / get_total(taxa_list, delim)
    taxa_tree = {
        'name': 'root',
        'parent': None,
        'size': 100,
        'children': {}
    }
    for taxon, abund in taxa_list.items():
        tkns = taxon.split(delim)
        recurse_tree(taxa_tree, tkns, 0, factor * abund)
    taxa_tree = convert_children_to_list(taxa_tree)
    return taxa_tree


class TaxaTreeWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.analysis_result.set_module_status(MODULE_NAME, 'W')
        analysis_group = sample_group.analysis_result

        collate_task = collate_samples.s(ReadStatsToolResultModule.name(),
                                         ['raw', 'microbial'],
                                         sample_group_id)
        persist_task = persist_result.s(analysis_group.uuid, MODULE_NAME)

        task_chain = chain(collate_task,
                           read_stats_reducer.s(),
                           persist_task)
        result = task_chain.delay()

        return result

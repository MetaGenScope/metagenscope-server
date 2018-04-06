"""Tasks to process HMP results."""

from numpy import percentile

from app.extensions import celery
from app.tool_results.hmp_sites import HmpSitesResultModule

from .models import HMPResult


def make_dist_table(hmp_results, site_names):
    """Make a table of distributions, one distribution per site."""
    sites = []
    for site_name in site_names:
        sites.append([])
        for hmp_result in hmp_results:
            sites[-1] += getattr(hmp_result, site_name)
    dists = [percentile(measurements, [0, 25, 50, 75, 100])
             for measurements in sites]
    return dists


@celery.task()
def make_distributions(samples, categories):
    """Determine HMP distributions by site and category."""
    tool_name = HmpSitesResultModule.name()
    site_names = HmpSitesResultModule.result_model().site_names()

    distributions = {}
    for cat_name, cat_vals in categories.items():
        tbl = {cat_val: [] for cat_val in cat_vals}
        for sample in samples:
            hmp_result = getattr(sample, tool_name)
            tbl[sample.metadata[cat_name]].append(hmp_result)
        distribution = {
            {'name': cat_val, 'data': make_dist_table(hmp_results, site_names)}
            for cat_val, hmp_results in tbl.items()
        }
        distributions[cat_name] = distribution

    return distributions, categories, site_names


@celery.task
def reducer_task(args):
    """Return an HMP result model from components."""
    distributions = args[0]
    categories = args[1]
    site_names = args[2]

    return HMPResult(categories=categories,
                     sites=site_names,
                     distributions=distributions)
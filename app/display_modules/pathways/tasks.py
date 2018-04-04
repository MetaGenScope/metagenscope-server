"""Tasks for pathways module."""

import pandas as pd
import numpy as np

from app.extensions import celery
from app.tool_results.humann2 import Humann2ResultModule

from .constants import TOP_N
from .models import PathwayResult


def pathways_from_sample(sample):
    """Get pathways from a humann2 result."""
    return getattr(sample, Humann2ResultModule.name()).pathways


def get_top_paths(sample_dict):
    """Return the names of the TOP_N most abundant paths."""
    def unwrap(path_tbl):
        """Return abundances from a path_tbl."""
        return {path_name: val.abundance
                for path_name, val in path_tbl.items()}

    abund_tbl = {sname: unwrap(path_tbl)
                 for sname, path_tbl in sample_dict.items()}
    abund_tbl = pd.DataFrame(abund_tbl).fillna(0)
    abund_mean = np.array(abund_tbl.mean(axis=0))

    idx = (-1 * abund_mean).argsort()[:TOP_N]
    path_names = set(abund_tbl.index[idx])
    return path_names


@celery.task()
def filter_humann2_pathways(samples):
    """Get the top N mean abundance pathways."""
    sample_dict = {sample.name: pathways_from_sample(sample)
                   for sample in samples}
    path_names = get_top_paths(sample_dict)
    assert path_names
    out = {}
    for sname, path_tbl in sample_dict.items():
        path_abunds = {}
        path_covs = {}
        for path_name in path_names:
            try:
                abund = path_tbl[path_name].abundance
                cov = path_tbl[path_name].coverage
            except KeyError:
                abund = 0
                cov = 0
            path_abunds[path_name] = abund
            path_covs[path_name] = cov

        out[sname] = {'pathway_abundances': path_abunds,
                      'pathway_coverages': path_covs}

    return PathwayResult(samples=out)

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


def get_abund_tbl(sample_dict):
    """Return a tbl of abundances and a vector of means."""
    abund_dict = {}
    for sname, path_tbl in sample_dict.items():
        abund_dict[sname] = {}
        for path_name, vals in path_tbl.items():
            abund_dict[sname][path_name] = vals['abundance']

    # Columns are samples, rows are pathways, vals are abundances
    abund_tbl = pd.DataFrame(abund_dict).fillna(0)
    abund_mean = np.array(abund_tbl.mean(axis=1))
    return abund_tbl, abund_mean


def get_top_paths(abund_tbl, abund_mean, top_n):
    """Return the names of the top_n most abundant paths."""
    assert len(abund_mean) == len(abund_tbl.index)
    idx = (-1 * abund_mean).argsort()[:top_n]
    path_names = set(abund_tbl.index[idx])
    return path_names


@celery.task()
def filter_humann2_pathways(samples):
    """Get the top N mean abundance pathways."""
    sample_dict = {sample.name: pathways_from_sample(sample)
                   for sample in samples}

    abund_tbl, abund_mean = get_abund_tbl(sample_dict)
    path_names = get_top_paths(abund_tbl, abund_mean, TOP_N)
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

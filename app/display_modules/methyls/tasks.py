"""Tasks for generating Methyl results."""

import numpy as np
import pandas as pd

from app.extensions import celery
from app.tool_results.methyltransferases import MethylResultModule

from .constants import TOP_N


def fill_gene_array(gene_array, gene_names):
    """Fill in missing gene names in gene_array with 0."""
    out = {}
    for gene_name in gene_names:
        try:
            out[gene_name] = gene_array[gene_names]
        except KeyError:
            out[gene_name] = 0
    return out


def transform_sample(sample_vals, gene_names):
    """Transform sample values to rpkm output."""
    out = {
        'rpkm': fill_gene_array(sample_vals.rpkm, gene_names),
        'rpkmg': fill_gene_array(sample_vals.rpkmg, gene_names),
    }
    return out


@celery.task()
def filter_methyl_results(samples):
    """Reduce Methyl results to the <TOP_N> mean abundance genes (rpkm)."""
    sample_dict = {sample.name: getattr(sample, MethylResultModule.name())
                   for sample in samples}
    rpkm_dict = {}
    for sname, gene_dict in sample_dict.items():
        rpkm_dict[sname] = {}
        for gene, vals in gene_dict.items():
            rpkm_dict[sname][gene][vals['rpkm']]

    # Columns are samples, rows are genes, vals are rpkms
    rpkm_tbl = pd.DataFrame(rpkm_dict).fillna(0)
    rpkm_mean = np.array(rpkm_tbl.mean(axis=0))

    idx = (-1 * rpkm_mean).argsort()[:TOP_N]
    gene_names = set(rpkm_tbl.index.iloc[idx])

    filtered_sample_tbl = {sname: transform_sample(vfdb, gene_names)
                           for sname, vfdb in sample_dict.items()}

    return {'samples': filtered_sample_tbl}

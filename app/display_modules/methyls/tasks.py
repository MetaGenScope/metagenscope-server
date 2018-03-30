"""Tasks for generating Methyl results."""

import numpy as np
import pandas as pd

from app.extensions import celery
from app.tool_results.methyltransferases import MethylResultModule

from .models import MethylResult
from .constants import TOP_N


def transform_sample(methyl_tool_result, gene_names):
    """Transform sample values to rpkm output."""
    out = {'rpkm': {}, 'rpkmg': {}}
    for gene_name in gene_names:
        try:
            vals = methyl_tool_result.genes[gene_name]
            rpkm, rpkmg = vals['rpkm'], vals['rpkmg']
        except KeyError:
            rpkm, rpkmg = 0, 0
        out['rpkm'][gene_name] = rpkm
        out['rpkmg'][gene_name] = rpkmg
    return out


@celery.task()
def filter_methyl_results(samples):
    """Reduce Methyl results to the <TOP_N> mean abundance genes (rpkm)."""
    sample_dict = {sample.name: getattr(sample, MethylResultModule.name())
                   for sample in samples}
    rpkm_dict = {}
    for sname, methyl_tool_result in sample_dict.items():
        rpkm_dict[sname] = {}
        for gene, vals in methyl_tool_result.genes.items():
            rpkm_dict[sname][gene] = vals['rpkm']

    # Columns are samples, rows are genes, vals are rpkms
    rpkm_tbl = pd.DataFrame(rpkm_dict).fillna(0)
    rpkm_mean = np.array(rpkm_tbl.mean(axis=0))

    idx = (-1 * rpkm_mean).argsort()[:TOP_N]
    gene_names = set(rpkm_tbl.index[idx])

    filtered_sample_tbl = {sname: transform_sample(methyl_tool_result, gene_names)
                           for sname, methyl_tool_result in sample_dict.items()}

    return MethylResult(samples=filtered_sample_tbl)

"""Tasks to process Volcano results."""

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from app.display_modules.utils import persist_result_helper
from app.extensions import celery
from app.tool_results.card_amrs import CARDAMRResultModule
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.humann2 import Humann2ResultModule

from .models import VolcanoResult


def make_dataframe(samples, tool_name):
    """Return a pandas dataframe for the given tool."""
    tbl = {}
    for sample in samples:
        tbl[sample.name] = sample['tool_name']
    return pd.DataFrame(tbl, orient='index').fillna(0)


def get_cases(category_name, category_value, samples):
    """Return sets for case and control sample names."""
    cases, controls = set(), set()
    for sample in samples:
        if sample.metadata[category_name] == category_value:
            cases.add(sample.name)
            continue
        controls.add(sample.name)
    return cases, controls


def get_lfcs(df, cases, controls):
    """Return two series: LFC of means and mean of cases."""
    caseMeans = df.loc[cases].mean(index=1)
    controlMeans = df.loc[controls].mean(index=1)
    lfcs = (caseMeans / controlMeans).apply(np.log2)
    return lfcs, caseMeans


def get_nlps(df, cases, controls):
    """Return a series of nlps for each column and a list of raw pvalues."""
    ps = []

    def mwu(col):
        """Perform MWU test on a column of the dataframe."""
        _, p = mannwhitneyu(col[cases], col[controls])
        p *= 2  # correct for two sided
        assert p <= 1.0
        ps.append(p)
        nlp = -np.log10(p)
        return nlp

    nlps = df.apply(mwu, imdex=1)
    return nlps, ps


def pval_hist(ps, bin_width=0.05):
    """Return a histogram of pvalues."""
    nBins = int(1 / bin_width + 0.5)
    bins = {bin_width * i: 0
            for i in range(nBins)}
    for p in ps:
        for bin_start in bins:
            bin_end = bin_start + bin_width
            if (p >= bin_start) and (p < bin_end):
                bins[bin_start] += 1
                break

    pts = [{'x': bin_start, 'y': nps}
           for bin_start, nps in bins.items()]
    return pts


def handle_one_tool_category(category_name, category_value, samples, tool_name):
    """Return the JSON for a ToolCategoryDocument."""
    df = make_dataframe(samples, tool_name)
    cases, controls = get_cases(category_name, category_value, samples)
    lfcs, caseMeans = get_lfcs(df, cases, controls)
    nlps, ps = get_nlps(df, cases, controls)

    out = {
        'scatter_plot': pd.concat({
            'x': lfcs,
            'y': nlps,
            'z': caseMeans,
            'name': df.index,
        }).to_dict(orient='records'),
        'pval_histogram': pval_hist(ps)
    }
    return out


@celery.task()
def make_volcanos(categories, samples):
    """Return the JSON for a VolcanoResult."""
    tool_names = [
        CARDAMRResultModule.name(),
        KrakenResultModule.name(),
        Metaphlan2ResultModule.name(),
        Humann2ResultModule.name(),
    ]
    out = {'categories': categories}
    for tool_name in tool_names:
        out['tools'][tool_name]['tool_categories'] = {}
        tool_tbl = out['tools'][tool_name]['tool_categories']
        for category_name, category_values in categories.items():
            tool_tbl[category_name] = {}
            for category_value in category_values:
                tool_tbl[category_value] = handle_one_tool_category(
                    category_name,
                    category_value,
                    samples,
                    tool_name,
                )
    return out


@celery.task(name='volcano.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Microbe Directory results."""
    result = VolcanoResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)

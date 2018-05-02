# pylint: disable=invalid-name

"""MetaGenScope seed data from ARBF 2017."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper

from .loader import (
    load_sample_similarity,
    load_taxon_abundance,
    load_reads_classified,
    load_hmp,
    load_ags,
)


sample_similarity = AnalysisResultWrapper(status='S', data=load_sample_similarity())
taxon_abundance = AnalysisResultWrapper(status='S', data=load_taxon_abundance())
hmp = AnalysisResultWrapper(status='S', data=load_hmp())
ags = AnalysisResultWrapper(status='S', data=load_ags())

abrf_analysis_result = AnalysisResultMeta(sample_similarity=sample_similarity,
                                          taxon_abundance=taxon_abundance,
                                          hmp=hmp,
                                          average_genome_size=ags)

# pylint: disable=invalid-name

"""MetaGenScope seed data."""


from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from seed.abrf_2017 import (
    load_sample_similarity,
    load_taxon_abundance,
    load_reads_classified,
    load_hmp,
)


sample_similarity = AnalysisResultWrapper(status='S', data=load_sample_similarity())
taxon_abundance = AnalysisResultWrapper(status='S', data=load_taxon_abundance())
reads_classified = AnalysisResultWrapper(status='S', data=load_reads_classified())
hmp = AnalysisResultWrapper(status='S', data=load_hmp())

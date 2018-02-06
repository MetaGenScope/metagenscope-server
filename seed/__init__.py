"""MetaGenScope seed data."""


from app.query_results.query_result_models import (
    SampleSimilarityResultWrapper,
    TaxonAbundanceResultWrapper,
    ReadsClassifiedResultWrapper,
    HMPResultWrapper,
)
from seed.abrf_2017 import (
    load_sample_similarity,
    load_taxon_abundance,
    load_reads_classified,
    load_hmp,
)


sample_similarity = SampleSimilarityResultWrapper(status='S', data=load_sample_similarity())
taxon_abundance = TaxonAbundanceResultWrapper(status='S', data=load_taxon_abundance())
reads_classified = ReadsClassifiedResultWrapper(status='S', data=load_reads_classified())
hmp = HMPResultWrapper(status='S', data=load_hmp())

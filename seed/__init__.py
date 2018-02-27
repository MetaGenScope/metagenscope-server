"""MetaGenScope seed data."""


from app.api.v1.display_modules.hmp_module import HMPModule
from app.api.v1.display_modules.reads_classified_module import ReadsClassifiedModule
from app.api.v1.display_modules.sample_similarity_module import SampleSimilarityDisplayModule
from app.api.v1.display_modules.taxon_abundance_module import TaxonAbundanceDisplayModule

from seed.abrf_2017 import (
    load_sample_similarity,
    load_taxon_abundance,
    load_reads_classified,
    load_hmp,
)


SampleSimilarityResultWrapper = SampleSimilarityDisplayModule.get_query_result_wrapper()
TaxonAbundanceResultWrapper = TaxonAbundanceDisplayModule.get_query_result_wrapper()
ReadsClassifiedResultWrapper = ReadsClassifiedModule.get_query_result_wrapper()
HMPResultWrapper = HMPModule.get_query_result_wrapper()

sample_similarity = SampleSimilarityResultWrapper(status='S', data=load_sample_similarity())
taxon_abundance = TaxonAbundanceResultWrapper(status='S', data=load_taxon_abundance())
reads_classified = ReadsClassifiedResultWrapper(status='S', data=load_reads_classified())
hmp = HMPResultWrapper(status='S', data=load_hmp())

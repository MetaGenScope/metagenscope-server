"""MetaGenScope seed data."""


from app.display_modules.hmp import HMPModule
from app.display_modules.reads_classified import ReadsClassifiedModule
from app.display_modules.sample_similarity import SampleSimilarityDisplayModule
from app.display_modules.taxon_abundance import TaxonAbundanceDisplayModule

from seed.abrf_2017 import (
    load_sample_similarity,
    load_taxon_abundance,
    load_reads_classified,
    load_hmp,
)


SampleSimilarityResultWrapper = SampleSimilarityDisplayModule.get_analysis_result_wrapper()
TaxonAbundanceResultWrapper = TaxonAbundanceDisplayModule.get_analysis_result_wrapper()
ReadsClassifiedResultWrapper = ReadsClassifiedModule.get_analysis_result_wrapper()
HMPResultWrapper = HMPModule.get_analysis_result_wrapper()

# pylint: disable=invalid-name
sample_similarity = SampleSimilarityResultWrapper(status='S', data=load_sample_similarity())
taxon_abundance = TaxonAbundanceResultWrapper(status='S', data=load_taxon_abundance())
reads_classified = ReadsClassifiedResultWrapper(status='S', data=load_reads_classified())
hmp = HMPResultWrapper(status='S', data=load_hmp())

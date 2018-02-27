"""Collect display modules."""

from app.api.v1.display_modules.hmp_module import HMPModule
from app.api.v1.display_modules.reads_classified_module import ReadsClassifiedModule
from app.api.v1.display_modules.sample_similarity_module import SampleSimilarityDisplayModule
from app.api.v1.display_modules.taxon_abundance_module import TaxonAbundanceDisplayModule

all_display_modules = [     # pylint: disable=invalid-name
    HMPModule,
    ReadsClassifiedModule,
    SampleSimilarityDisplayModule,
    TaxonAbundanceDisplayModule,
]

"""Collect display modules."""

from app.display_modules.hmp_module import HMPModule
from app.display_modules.reads_classified_module import ReadsClassifiedModule
from app.display_modules.sample_similarity_module import SampleSimilarityDisplayModule
from app.display_modules.taxon_abundance_module import TaxonAbundanceDisplayModule

all_display_modules = [     # pylint: disable=invalid-name
    HMPModule,
    ReadsClassifiedModule,
    SampleSimilarityDisplayModule,
    TaxonAbundanceDisplayModule,
]

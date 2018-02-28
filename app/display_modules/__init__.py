"""Collect display modules."""

from app.display_modules.hmp import HMPModule
from app.display_modules.reads_classified import ReadsClassifiedModule
from app.display_modules.sample_similarity import SampleSimilarityDisplayModule
from app.display_modules.taxon_abundance import TaxonAbundanceDisplayModule

all_display_modules = [     # pylint: disable=invalid-name
    HMPModule,
    ReadsClassifiedModule,
    SampleSimilarityDisplayModule,
    TaxonAbundanceDisplayModule,
]

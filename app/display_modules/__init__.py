"""Modules for converting analysis tool output to front-end display data."""

from app.display_modules.ags import AGSDisplayModule
from app.display_modules.hmp import HMPModule
from app.display_modules.microbe_directory import MicrobeDirectoryDisplayModule
from app.display_modules.pathways import PathwaysDisplayModule
from app.display_modules.reads_classified import ReadsClassifiedModule
from app.display_modules.sample_similarity import SampleSimilarityDisplayModule
from app.display_modules.taxon_abundance import TaxonAbundanceDisplayModule


all_display_modules = [  # pylint: disable=invalid-name
    AGSDisplayModule,
    HMPModule,
    MicrobeDirectoryDisplayModule,
    PathwaysDisplayModule,
    ReadsClassifiedModule,
    SampleSimilarityDisplayModule,
    TaxonAbundanceDisplayModule,
]

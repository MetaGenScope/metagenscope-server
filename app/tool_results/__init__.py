"""Modules for genomic analysis tool outputs."""

from .card_amrs import CARDAMRResultModule
from .food_pet import FoodPetResultModule
from .hmp_sites import HmpSitesResultModule
from .humann2 import Humann2ResultModule
from .humann2_normalize import Humann2NormalizeResultModule
from .kraken import KrakenResultModule
from .metaphlan2 import Metaphlan2ResultModule
from .methyltransferases import MethylResultModule
from .microbe_census import MicrobeCensusResultModule
from .microbe_directory import MicrobeDirectoryResultModule
from .read_stats import ReadStatsToolResultModule
from .reads_classified import ReadsClassifiedResultModule
from .shortbred import ShortbredResultModule
from .vfdb import VFDBResultModule


all_sample_results = [  # pylint: disable=invalid-name
    CARDAMRResultModule,
    FoodPetResultModule,
    HmpSitesResultModule,
    Humann2ResultModule,
    Humann2NormalizeResultModule,
    KrakenResultModule,
    Metaphlan2ResultModule,
    MethylResultModule,
    MicrobeCensusResultModule,
    MicrobeDirectoryResultModule,
    ReadStatsToolResultModule,
    ReadsClassifiedResultModule,
    ShortbredResultModule,
    VFDBResultModule,
]


all_group_results = []  # pylint: disable=invalid-name

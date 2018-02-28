"""Modules for genomic analysis tool outputs."""

from app.tool_modules.food_pet import FoodPetResult
from app.tool_modules.hmp_sites import HmpSitesResult
from app.tool_modules.kraken import KrakenResult
from app.tool_modules.metaphlan2 import Metaphlan2Result
from app.tool_modules.mic_census import MicCensusResult
from app.tool_modules.nanopore_taxa import NanoporeTaxaResult
from app.tool_modules.reads_classified import ReadsClassifiedResult
from app.tool_modules.shortbred import ShortbredResult


all_tool_modules = [    # pylint: disable=invalid-name
    FoodPetResult,
    HmpSitesResult,
    KrakenResult,
    Metaphlan2Result,
    MicCensusResult,
    NanoporeTaxaResult,
    ReadsClassifiedResult,
    ShortbredResult,
]

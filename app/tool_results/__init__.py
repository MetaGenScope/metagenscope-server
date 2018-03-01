"""Modules for genomic analysis tool outputs."""

# from app.tool_results.food_pet import FoodPetResultModule
from app.tool_results.hmp_sites import HmpSitesResultModule
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.mic_census import MicCensusResultModule
from app.tool_results.nanopore_taxa import NanoporeTaxaResultModule
from app.tool_results.reads_classified import ReadsClassifiedResultModule
from app.tool_results.shortbred import ShortbredResultModule

# Re-export modules
from app.tool_results.tool_module import ToolResult, ToolResultModule


all_tool_result_modules = [    # pylint: disable=invalid-name
    # FoodPetResultModule,     # Skip this module for now
    HmpSitesResultModule,
    KrakenResultModule,
    Metaphlan2ResultModule,
    MicCensusResultModule,
    NanoporeTaxaResultModule,
    ReadsClassifiedResultModule,
    ShortbredResultModule,
]

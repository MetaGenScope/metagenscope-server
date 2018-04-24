"""Create and save a Sample Group with all the fixings (plus gravy)."""

from uuid import uuid4

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.display_modules.ags.tests.factory import AGSFactory
from app.display_modules.card_amrs.tests.factory import CARDGenesFactory
from app.display_modules.functional_genes.tests.factory import FunctionalGenesFactory
from app.display_modules.hmp.tests.factory import HMPFactory
from app.display_modules.macrobes.tests.factory import MacrobeFactory
from app.display_modules.methyls.tests.factory import MethylsFactory
from app.display_modules.microbe_directory.tests.factory import MicrobeDirectoryFactory
from app.display_modules.pathways.tests.factory import PathwayFactory
from app.display_modules.read_stats.tests.factory import ReadStatsFactory
from app.display_modules.reads_classified.tests.factory import ReadsClassifiedFactory
from app.display_modules.sample_similarity.tests.factory import create_mvp_sample_similarity
from app.display_modules.virulence_factors.tests.factory import VFDBFactory
from app.sample_groups.sample_group_models import SampleGroup


def create_saved_group(uuid=None):
    """Create and save a Sample Group with all the fixings (plus gravy)."""
    if uuid is None:
        uuid = uuid4()
    analysis_result = AnalysisResultMeta().save()
    group_description = 'Includes factory-produced analysis results from all display_modules'
    sample_group = SampleGroup(name='Fuzz Testing',
                               analysis_result=analysis_result,
                               description=group_description)
    sample_group.id = uuid
    db.session.add(sample_group)
    db.session.commit()

    # Add the results
    analysis_result.average_genome_size = AGSFactory()
    analysis_result.card_amr_genes = CARDGenesFactory()
    analysis_result.functional_genes = FunctionalGenesFactory()
    analysis_result.hmp = HMPFactory()
    analysis_result.macrobe_abundance = MacrobeFactory()
    analysis_result.methyltransferases = MethylsFactory()
    analysis_result.microbe_directory = MicrobeDirectoryFactory()
    analysis_result.pathways = PathwayFactory()
    analysis_result.read_stats = ReadStatsFactory()
    analysis_result.reads_classified = ReadsClassifiedFactory()
    analysis_result.sample_similarity = create_mvp_sample_similarity()
    # analysis_result.taxon_abundance =
    analysis_result.virulence_factors = VFDBFactory()
    analysis_result.save()

    return sample_group

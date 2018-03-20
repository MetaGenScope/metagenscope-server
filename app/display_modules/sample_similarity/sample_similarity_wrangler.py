"""Tasks for generating Sample Similarity results."""

from celery import chord

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.sample_similarity.constants import MODULE_NAME
from app.display_modules.sample_similarity.sample_similarity_tasks import (
    taxa_tool_tsne,
    sample_similarity_reducer,
)
from app.display_modules.utils import categories_from_metadata, persist_result
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule


class SampleSimilarityWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather samples and process."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.set_module_status(MODULE_NAME, 'W')
        samples = sample_group.samples

        reducer = sample_similarity_reducer.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)

        categories_task = categories_from_metadata.s(samples)
        kraken_task = taxa_tool_tsne.s(samples, KrakenResultModule.name())
        metaphlan2_task = taxa_tool_tsne.s(samples, Metaphlan2ResultModule.name())
        middle_tasks = [categories_task, kraken_task, metaphlan2_task]

        return chord(middle_tasks)(reducer | persist_task)

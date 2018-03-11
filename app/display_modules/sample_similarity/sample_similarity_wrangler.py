"""Tasks for generating Sample Similarity results."""

from celery import group

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.sample_similarity.sample_similarity_tasks import (
    taxa_tool_tsne,
    sample_similarity_reducer,
)
from app.display_modules.utils import categories_from_metadata, fetch_samples
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule


class SampleSimilarityWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    @staticmethod
    def run_sample_group(sample_group_id):
        """Gather samples and process."""
        categories_task = categories_from_metadata.s()
        kraken_task = taxa_tool_tsne.s(KrakenResultModule.name())
        metaphlan2_task = taxa_tool_tsne.s(Metaphlan2ResultModule.name())

        middle_tasks = [categories_task, kraken_task, metaphlan2_task]
        tsne_chain = (fetch_samples.s() | group(middle_tasks) | sample_similarity_reducer.s())
        result = tsne_chain(sample_group_id)

        return result

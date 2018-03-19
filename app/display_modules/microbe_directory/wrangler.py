"""Wrangler for Microbe Directory results."""

from celery import chain

from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result, collate_samples
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.microbe_directory import MicrobeDirectoryResultModule

from .constants import MODULE_NAME
from .tasks import microbe_directory_reducer


class MicrobeDirectoryWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    fields = ['antimicrobial_susceptibility',
              'plant_pathogen',
              'optimal_temperature',
              'optimal_ph',
              'animal_pathogen',
              'microbiome_location',
              'biofilm_forming',
              'spore_forming',
              'pathogenicity',
              'extreme_environment',
              'gram_stain']

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()

        # Set state on Analysis Group
        analysis_group = sample_group.analysis_result
        wrapper = AnalysisResultWrapper(status='W')
        setattr(analysis_group, MODULE_NAME, wrapper)
        analysis_group.save()

        tool_result_name = MicrobeDirectoryResultModule.name()
        collate_task = collate_samples.s(tool_result_name, cls.fields, sample_group_id)
        reducer_task = microbe_directory_reducer.s()
        persist_task = persist_result.s(analysis_group.uuid, MODULE_NAME)

        task_chain = chain(collate_task, reducer_task, persist_task)
        result = task_chain.delay()

        return result

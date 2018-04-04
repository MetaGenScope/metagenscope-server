"""The base Display Module Wrangler module."""

from app.analysis_results.analysis_result_models import AnalysisResultWrapper


class DisplayModuleWrangler:
    """The base Display Module Wrangler module."""

    @classmethod
    def run_sample(cls, sample_id):
        """Gather single sample and process."""
        pass

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather group of samples and process."""
        pass

    @classmethod
    def set_analysis_group_state(cls, module_name, sample_group):
        """Set state on Analysis Group the return that group."""
        analysis_group = sample_group.analysis_result
        wrapper = AnalysisResultWrapper(status='W')
        setattr(analysis_group, module_name, wrapper)
        analysis_group.save()
        return analysis_group

"""Create and save a Sample Group with all the fixings (plus gravy)."""

from app import db

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.display_modules.ags.tests.factory import AGSFactory
from app.sample_groups.sample_group_models import SampleGroup


def create_saved_group():
    """Create and save a Sample Group with all the fixings (plus gravy)."""
    analysis_result = AnalysisResultMeta().save()
    group_description = 'Includes factory-produced analysis results from all display_modules'
    sample_group = SampleGroup(name='Fuzz Testing',
                               analysis_result=analysis_result,
                               description=group_description)
    db.session.add(sample_group)
    db.session.commit()

    # Add the results
    analysis_result.ags = AGSFactory()
    analysis_result.save()

    return sample_group

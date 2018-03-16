"""Display module utilities."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.extensions import celery
from app.sample_groups.sample_group_models import SampleGroup


@celery.task()
def categories_from_metadata(samples, min_size=2):
    """
    Create dict of categories and their values from sample metadata.

    Parameters
    ----------
    samples : list
        List of sample models.
    min_size: int
        Minimum number of values required for a given metadata item to
        be included in returned categories.

    Returns
    -------
    dict
        Dictionary of form {<category_name>: [category_value[, category_value]]}

    """
    categories = {}

    # Gather categories and values
    all_metadata = [sample.metadata for sample in samples]
    for metadata in all_metadata:
        properties = [prop for prop in metadata.keys()]
        for prop in properties:
            if prop not in categories:
                categories[prop] = set([])
            categories[prop].add(metadata[prop])

    # Filter for minimum number of values
    categories = {category_name: category_values
                  for category_name, category_values in categories.items()
                  if len(category_values) >= min_size}

    return categories


@celery.task()
def fetch_samples(sample_group_id):
    """Return sample list for a SampleGroup based on ID."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
    samples = sample_group.samples
    return samples


@celery.task()
def persist_result(analysis_result_id, result_name, result):
    """Persist results to an Analysis Result model."""
    analysis_result = AnalysisResultMeta.objects.get(uuid=analysis_result_id)
    wrapper = getattr(analysis_result, result_name)
    wrapper.data = result
    wrapper.status = 'S'
    analysis_result.save()

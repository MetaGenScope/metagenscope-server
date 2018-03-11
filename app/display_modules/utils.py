"""Display module utilities."""

from app.analysis_results.analysis_result_models import (
    AnalysisResultWrapper,
    AnalysisResultMeta,
)
from app.extensions import celery, mongoDB
from app.sample_groups.sample_group_models import SampleGroup


def create_result_wrapper(wrapper_name, model_cls):
    """Create wrapper for analysis result data field."""
    mongo_field = mongoDB.EmbeddedDocumentField(model_cls)
    # Create wrapper class
    return type(wrapper_name,
                (AnalysisResultWrapper,),
                {'data': mongo_field})


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
        properties = [prop for prop in vars(metadata)]
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
    analysis_result.save()

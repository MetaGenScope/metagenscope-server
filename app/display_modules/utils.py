"""Display module utilities."""


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

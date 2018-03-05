"""API helper methods."""

from functools import wraps

from mongoengine.errors import ValidationError


def handle_mongo_lookup(response, object_name):
    """Handle errors from fetching single Mongo object by ID."""
    def wrapper(f):     # pylint: disable=invalid-name,missing-docstring
        @wraps(f)
        def decorated(*args, **kwargs):     # pylint: disable=missing-docstring
            try:
                return f(*args, **kwargs)
            except IndexError:
                response.message = f'{object_name} does not exist.'
                response.code = 404
            except ValidationError as validation_error:
                response.message = f'{validation_error}'
                response.code = 400
            return response.json_and_code()
        return decorated
    return wrapper

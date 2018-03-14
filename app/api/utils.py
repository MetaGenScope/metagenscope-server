"""API helper methods."""

from functools import wraps

from flask_api.exceptions import NotFound, ParseError
from mongoengine.errors import ValidationError
from mongoengine import DoesNotExist


def handle_mongo_lookup(object_name):
    """Handle errors from fetching single Mongo object by ID."""
    def wrapper(f):     # pylint: disable=invalid-name,missing-docstring
        @wraps(f)
        def decorated(*args, **kwargs):     # pylint: disable=missing-docstring
            try:
                return f(*args, **kwargs)
            except DoesNotExist:
                raise NotFound(f'{object_name} does not exist.')
            except ValueError as value_error:
                if str(value_error) == 'badly formed hexadecimal UUID string':
                    raise ParseError('Invalid UUID provided.')
                raise value_error
            except ValidationError as validation_error:
                raise ParseError(str(validation_error))
        return decorated
    return wrapper

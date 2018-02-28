"""API helper methods."""

import base64

from functools import wraps
from uuid import UUID

from mongoengine.errors import ValidationError


# Based on https://stackoverflow.com/a/12270917
def uuid2slug(uuid):
    """Convert UUID to URL-safe base64 encoded slug."""
    if not isinstance(uuid, UUID):
        uuid = UUID(uuid)
    base64_uuid = base64.urlsafe_b64encode(uuid.bytes)
    return base64_uuid.decode('utf-8').rstrip('=\n').replace('/', '_')


def slug2uuid(slug):
    """Convert URL-safe base64 encoded slug to UUID."""
    return UUID(bytes=base64.urlsafe_b64decode((slug + '==').replace('_', '/')))


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

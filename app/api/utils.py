"""API helper methods."""

import base64

from uuid import UUID


# Based on https://stackoverflow.com/a/12270917
def uuid2slug(uuidstring):
    """Convert UUID string to URL-safe base64 encoded slug."""
    base64_uuid = base64.urlsafe_b64encode(UUID(uuidstring).bytes)
    return base64_uuid.decode('utf-8').rstrip('=\n').replace('/', '_')


def slug2uuid(slug):
    """Convert URL-safe base64 encoded slug to UUID string."""
    return str(UUID(bytes=base64.urlsafe_b64decode((slug + '==').replace('_', '/'))))

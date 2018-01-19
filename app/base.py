"""Base modules used throughout application."""

from uuid import UUID
from marshmallow import Schema, pre_load, post_load, pre_dump, post_dump

from app.api.utils import uuid2slug


class BaseSchema(Schema):
    """Base Schema that handles envelopes and slug generation."""

    __envelope__ = {
        'single': None,
        'many': None
    }

    def get_envelope_key(self, many):
        """Help get the envelope key."""
        key = self.__envelope__['many'] if many else self.__envelope__['single']
        assert key is not None, 'Envelope key undefined'
        return key

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many):
        """Unwrap envelope."""
        key = self.get_envelope_key(many)
        return data[key]

    @post_load
    def make_object(self, data):
        """Make object from unwrapped envelope."""
        # pylint: disable=no-member
        return self.__model__(**data)

    @pre_dump(pass_many=False)
    # pylint: disable=no-self-use
    def slugify_organization_id(self, data):
        """Translate UUID into URL-safe slug."""
        if hasattr(data, 'id') and isinstance(data.id, UUID):
            data.slug = uuid2slug(data.id)
        return data

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        """Wrap data with envelope."""
        key = self.get_envelope_key(many)
        return {key: data}

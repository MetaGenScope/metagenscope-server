"""Base modules used throughout application."""

from uuid import UUID

from marshmallow import Schema, pre_load, post_load, pre_dump, post_dump


class BaseSchema(Schema):
    """Base Schema that handles envelopes."""

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
        return self.__model__(**data)  # pylint: disable=no-member

    @pre_dump(pass_many=False)
    def standardize_uuid_property(self, data):  # pylint: disable=no-self-use
        """Rename id properties into standardized uuid field."""
        if hasattr(data, 'id') and isinstance(data.id, UUID):
            data.uuid = data.id
        return data

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        """Wrap data with envelope."""
        key = self.get_envelope_key(many)
        return {key: data}

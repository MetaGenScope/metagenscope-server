"""Reads Classified display module."""

from mongoengine import ValidationError

from app.api.v1.display_modules.display_module import DisplayModule
from app.extensions import mongoDB as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField   # pylint: disable=invalid-name


class ReadsClassifiedModule(DisplayModule):
    """Reads Classified display module."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return 'reads_classified'

    @classmethod
    def get_query_result_wrapper_field(cls):
        """Return status wrapper for Reads Classified type."""
        return EmbeddedDoc(ReadsClassifiedResult)


class ReadsClassifiedDatum(mdb.EmbeddedDocument):       # pylint: disable=too-few-public-methods
    """Taxon Abundance datum type."""

    category = mdb.StringField(required=True)
    values = mdb.ListField(mdb.FloatField(), required=True)


class ReadsClassifiedResult(mdb.EmbeddedDocument):      # pylint: disable=too-few-public-methods
    """Reads Classified document type."""

    categories = mdb.ListField(mdb.StringField(), required=True)
    sample_names = mdb.ListField(mdb.StringField(), required=True)
    data = mdb.EmbeddedDocumentListField(ReadsClassifiedDatum, required=True)

    def clean(self):
        """Ensure integrity of result content."""
        for datum in self.data:
            if datum.category not in self.categories:
                msg = f'Datum category \'{datum.category}\' does not exist in categories!'
                raise ValidationError(msg)
            if len(datum.values) != len(self.sample_names):
                msg = (f'Number of datum values for \'{datum.category}\''
                       'does not match sample_names length!')
                raise ValidationError(msg)

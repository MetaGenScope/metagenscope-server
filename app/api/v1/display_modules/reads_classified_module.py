from .display_module import DisplayModule
from app.extensions import mongoDB as mdb
from mongoengine import ValidationError

EmDoc = mdb.EmbeddedDocumentField


class ReadsClassifiedModule(DisplayModule):

    @classmethod
    def name(ctype):
        return 'reads_classified'

    @classmethod
    def get_data(ctype, my_result):
        return my_result

    @classmethod
    def get_query_result_wrapper_field(ctype):
        return EmDoc(ReadsClassifiedResult)

    @classmethod
    def get_mongodb_embedded_docs(ctype):
        return [ReadsClassifiedDatum,
                ReadsClassifiedResult]


class ReadsClassifiedDatum(mdb.EmbeddedDocument):
    """Taxon Abundance datum type."""

    category = mdb.StringField(required=True)
    values = mdb.ListField(mdb.FloatField(), required=True)


class ReadsClassifiedResult(mdb.EmbeddedDocument):
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

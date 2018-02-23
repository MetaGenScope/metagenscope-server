from .display_module import DisplayModule
from app.extensions import mongoDB as mdb
from mongoengine import ValidationError

EmDoc = mdb.EmbeddedDocumentField
EmDocList = mdb.EmbeddedDocumentListField
StringList = mdb.ListField(mdb.StringField())


class HMPModule(DisplayModule):

    @classmethod
    def name(ctype):
        return 'hmp'

    @classmethod
    def get_data(ctype, my_result):
        return my_result

    @classmethod
    def get_query_result_wrapper_field(ctype):
        return EmDoc(HMPResult)

    @classmethod
    def get_mongodb_embedded_docs(ctype):
        return [HMPDatum,
                HMPResult]


class HMPDatum(mdb.EmbeddedDocument):
    """HMP datum type."""

    name = mdb.StringField(required=True)
    data = mdb.ListField(mdb.ListField(mdb.FloatField()), required=True)


class HMPResult(mdb.EmbeddedDocument):
    """HMP document type."""

    categories = mdb.MapField(field=StringList, required=True)
    sites = mdb.ListField(mdb.StringField(), required=True)
    data = mdb.MapField(field=mdb.EmDocList(HMPDatum), required=True)

    def clean(self):
        """Ensure integrity of result content."""
        for category, values in self.categories.items():
            if category not in self.data:
                msg = f'Value \'{category}\' is not present in \'data\'!'
                raise ValidationError(msg)
            values_present = [datum.name for datum in self.data[category]]
            for value in values:
                if value not in values_present:
                    msg = f'Value \'{category}\' is not present in \'data\'!'
                    raise ValidationError(msg)

        for category_name, category_data in self.data.items():
            if len(category_data) != len(self.categories[category_name]):
                msg = (f'Category data for {category_name} does not match size of '
                       f'category values ({len(self.categories[category_name])})!')
                raise ValidationError(msg)
            for datum in category_data:
                if len(datum.data) != len(self.sites):
                    msg = (f'Datum <{datum.name}> of size {len(datum.data)} '
                           f'does not match size of sites ({len(self.sites)})!')
                    raise ValidationError(msg)

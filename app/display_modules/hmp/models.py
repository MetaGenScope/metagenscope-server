"""HMP display models."""

from mongoengine import ValidationError

from app.extensions import mongoDB as mdb


# Define aliases
EmDocList = mdb.EmbeddedDocumentListField       # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class HMPDatum(mdb.EmbeddedDocument):       # pylint: disable=too-few-public-methods
    """HMP datum type."""

    name = mdb.StringField(required=True)
    data = mdb.ListField(mdb.ListField(mdb.FloatField()), required=True)


class HMPResult(mdb.EmbeddedDocument):      # pylint: disable=too-few-public-methods
    """HMP document type."""

    categories = mdb.MapField(field=StringList, required=True)
    sites = mdb.ListField(mdb.StringField(), required=True)
    data = mdb.MapField(field=EmDocList(HMPDatum), required=True)

    def clean(self):
        """Ensure integrity of result content."""
        for category, values in self.categories.items():
            if category not in self.data:
                msg = f'Category \'{category}\' is not present in \'data\'!'
                raise ValidationError(msg)
            values_present = [datum.name for datum in self.data[category]]
            for value in values:
                if value not in values_present:
                    msg = f'Value \'{value}\' is not present in \'data\'!'
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

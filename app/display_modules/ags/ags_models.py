# pylint: disable=too-few-public-methods

"""Average Genome Size display models."""

from mongoengine import ValidationError

from app.extensions import mongoDB as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class DistributionResult(mdb.EmbeddedDocument):
    """Distribution for a boxplot."""

    min_val = mdb.FloatField(required=True)
    q1_val = mdb.FloatField(required=True)
    mean_val = mdb.FloatField(required=True)
    q3_val = mdb.FloatField(required=True)
    max_val = mdb.FloatField(required=True)

    def clean(self):
        """Ensure distribution is ordered."""
        values = [self.min_val, self.q1_val, self.mean_val,
                  self.q3_val, self.max_val]
        sorted_values = sorted(values)
        for value, sorted_value in zip(values, sorted_values):
            if value != sorted_value:
                raise ValidationError('Distribution is not in order.')


class AGSResult(mdb.EmbeddedDocument):
    """AGS document type."""

    # Categories dict has form: {<category_name>: [<category_value>, ...]}
    categories = mdb.MapField(field=StringList, required=True)
    # Distribution dict has form: {<category_name>: {<category_value>: <dist>}}
    distributions = mdb.MapField(field=mdb.MapField(field=EmbeddedDoc(DistributionResult)),
                                 required=True)

    def clean(self):
        """Skip validation on this result model."""
        pass

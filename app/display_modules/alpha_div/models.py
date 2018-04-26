# pylint: disable=too-few-public-methods

"""Models for AlphaDiversity Display Module."""

from app.extensions import mongoDB as mdb

# Define aliases
EmDoc = mdb.EmbeddedDocumentField               # pylint: disable=invalid-name
EmDocList = mdb.EmbeddedDocumentListField       # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name
FloatList = mdb.ListField(mdb.FloatField())     # pylint: disable=invalid-name


class AlphaDiversityDatum(mdb.EmbeddedDocument):
    """AlphaDiv datum type."""

    metrics = StringList
    category_value = mdb.StringField(required=True)
    # metric -> distribution
    by_metric = mdb.MapField(field=FloatList)


class AlphaDiversityRank(mdb.EmbeddedDocument):
    """Store a map of cat_name -> [(cat_value, metric -> distribution)]."""

    by_category_name = mdb.MapField(field=EmDocList(AlphaDiversityDatum),
                                    required=True)


class AlphaDiversityTool(mdb.EmbeddedDocument):
    """Store a map of rank -> AlphaDiversityRank."""

    taxa_ranks = StringList
    by_taxa_rank = mdb.MapField(field=EmDoc(AlphaDiversityRank))


class AlphaDiversityResult(mdb.EmbeddedDocument):
    """Embedded results for alpha diversity."""

    # Categories dict has form: {<category_name>: [<category_value>, ...]}
    categories = mdb.MapField(field=StringList, required=True)
    tool_names = StringList
    by_tool = mdb.MapField(field=EmDoc(AlphaDiversityTool), required=True)

"""Tool Result model definitions."""


from app.extensions import mongoDB


class Result(mongoDB.Document):
    """Base mongo result class."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False)
    sampleId = mongoDB.StringField()
    toolId = mongoDB.StringField()
    sampleName = mongoDB.StringField()

    meta = {'allow_inheritance': True}


class Metaphlan2Result(Result):
    """Metaphlan 2 tool's result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


class ShortbredResult(Result):
    """Shortbred tool's result type."""

    abundances = mongoDB.DictField()


class MicCensusResult(Result):
    """Mic Census tool's result type."""

    average_genome_size = mongoDB.IntField()
    total_bases = mongoDB.IntField()
    genome_equivalents = mongoDB.IntField()


class KrakenResult(Result):
    """Kraken tool's result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


class NanoporeTaxaResult(Result):
    """Nanopore tool's taxa result type."""

    # The taxa dict is a map from taxon name to abundance value
    taxa = mongoDB.DictField()


class ReadsClassifiedResult(Result):
    """Reads Classified tool's result type."""

    viral = mongoDB.IntField()
    archaea = mongoDB.IntField()
    bacteria = mongoDB.IntField()
    host = mongoDB.IntField()
    unknown = mongoDB.IntField()


class HmpSitesResult(Result):
    """HMP Sites tool's result type."""

    gut = mongoDB.IntField()
    skin = mongoDB.IntField()
    throat = mongoDB.IntField()


class FoodPetResult(Result):
    """Food/Pet tool's result type."""

    vegetables = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    fruits = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    pets = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    meats = mongoDB.ListField(mongoDB.DictField(default={}), default=[])
    total_reads = mongoDB.IntField()

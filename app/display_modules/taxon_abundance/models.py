"""Taxon Abundance display module."""

from mongoengine import ValidationError

from app.extensions import mongoDB as mdb


class TaxonAbundanceNode(mdb.EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Taxon Abundance node type."""

    id = mdb.StringField(required=True)
    name = mdb.StringField(required=True)
    value = mdb.FloatField(required=True)


class TaxonAbundanceEdge(mdb.EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Taxon Abundance edge type."""

    source = mdb.StringField(required=True)
    target = mdb.StringField(required=True)
    value = mdb.FloatField(required=True)


class TaxonAbundanceFlow(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Taxon Abundance document type."""

    # Do not store depth of node because this can be derived from the edges
    nodes = mdb.EmbeddedDocumentListField(
        mdb.ListField(TaxonAbundanceNode()),
        required=True
    )
    edges = mdb.EmbeddedDocumentListField(TaxonAbundanceEdge, required=True)

    def clean(self):
        """Ensure that `edges` reference valid nodes."""
        node_ids = set([node.id for node in self.nodes])
        for edge in self.edges:
            if edge.source not in node_ids:
                msg = f'Could not find Edge source [{edge.source}] in nodes!'
                raise ValidationError(msg)
            if edge.target not in node_ids:
                msg = f'Could not find Edge target [{edge.target}] in nodes!'
                raise ValidationError(msg)


class TaxonAbundanceResult(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Taxon Abundance document type."""

    metaphlan2 = mdb.EmbeddedDocumentField(TaxonAbundanceFlow)
    kraken = mdb.EmbeddedDocumentField(TaxonAbundanceFlow)

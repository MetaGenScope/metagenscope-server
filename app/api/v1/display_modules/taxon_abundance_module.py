"""Taxon Abundance display module."""

from mongoengine import ValidationError

from app.api.v1.display_modules.display_module import DisplayModule
from app.extensions import mongoDB as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name


class TaxonAbundanceDisplayModule(DisplayModule):
    """Taxon Abundance display module."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return 'taxon_abundance'

    @classmethod
    def get_query_result_wrapper_field(cls):
        """Return status wrapper for Taxon Abundance type."""
        return EmbeddedDoc(TaxonAbundanceResult)


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


class TaxonAbundanceResult(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Taxon Abundance document type."""

    # Do not store depth of node because this can be derived from the edges
    nodes = mdb.EmbeddedDocumentListField(TaxonAbundanceNode, required=True)
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

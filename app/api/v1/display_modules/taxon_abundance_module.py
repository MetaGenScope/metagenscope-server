from .display_module import DisplayModule
from app.extensions import mongoDB as mdb
from mongoengine import ValidationError

EmDoc = mdb.EmbeddedDocumentField


class TaxonAbundanceDisplayModule(DisplayModule):

    @classmethod
    def name(ctype):
        return 'taxon_abundance'

    @classmethod
    def get_data(ctype, my_result):
        return my_result

    @classmethod
    def get_query_result_wrapper_field(ctype):
        return EmDoc(TaxonAbundanceResult)

    @classmethod
    def get_mongodb_embedded_docs(ctype):
        return [TaxonAbundanceEdge,
                TaxonAbundanceNode,
                TaxonAbundanceResult]


class TaxonAbundanceNode(mdb.EmbeddedDocument):
    """Taxon Abundance node type."""

    id = mdb.StringField(required=True)
    name = mdb.StringField(required=True)
    value = mdb.FloatField(required=True)


class TaxonAbundanceEdge(mdb.EmbeddedDocument):
    """Taxon Abundance edge type."""

    source = mdb.StringField(required=True)
    target = mdb.StringField(required=True)
    value = mdb.FloatField(required=True)


class TaxonAbundanceResult(mdb.EmbeddedDocument):
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

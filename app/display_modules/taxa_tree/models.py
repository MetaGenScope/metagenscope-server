"""Taxa Tree display models."""

from app.extensions import mongoDB as mdb
from mongoengine import ValidationError


def validate_json_tree(root, parent=None):
    if 'name' not in root:
        raise ValidationError('Node does not contain name field')

    if 'size' not in root:
        raise ValidationError('Node does not contain size field')
    else:
        try:
            float(root['size'])
        except ValueError:
            raise ValidationError('Size is not a float')

    if 'parent' not in root:
        raise ValidationError('Node does not contain parent field')
    elif parent and (root['parent'] != parent):
        raise ValidationError('Listed parent does not match structural parent')

    if 'children' not in root:
        raise ValidationError('Node does not contain children field')

    for child in root['children']:
        validate_json_tree(child, parent=root['name'])


class TaxaTreeResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    metaphlan2 = mdb.MapField(field=mdb.DynamicField(), required=True)
    kraken = mdb.MapField(field=mdb.DynamicField(), required=True)

    def clean(self):
        validate_json_tree(self.metaphlan2)
        validate_json_tree(self.kraken)

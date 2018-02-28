"""Tool Module base model definition."""


from app.extensions import mongoDB


class ToolModule(mongoDB.Document):
    """Base mongo result class."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False)
    sampleId = mongoDB.StringField()
    toolId = mongoDB.StringField()
    sampleName = mongoDB.StringField()

    meta = {'allow_inheritance': True}

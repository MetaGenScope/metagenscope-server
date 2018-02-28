"""Base module for Tool Results."""

from flask import request

from app.extensions import mongoDB
from app.api.endpoint_response import EndpointResponse


class ToolResult(mongoDB.Document):
    """Base mongo result class."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False)
    sampleId = mongoDB.StringField()
    toolId = mongoDB.StringField()
    sampleName = mongoDB.StringField()

    meta = {'allow_inheritance': True}


class ToolResultModule:
    """Base module for Tool Results."""

    @classmethod
    def name(cls):
        """Return Tool Result module's unique identifier string."""
        raise NotImplementedError()

    @classmethod
    def receive_upload(cls, sample_id):
        """Define handler for receiving uploads of analysis tool results."""
        response = EndpointResponse()
        # TODO: Check Sample exists
        print(sample_id)
        # TODO: Upsert data
        post_data = request.get_json()
        print(post_data)
        # TODO: Return whether it was inserted or updated (?)
        return response.json_and_code()

    @classmethod
    def register_api_call(cls, router):
        """Register API endpoint for this display module type."""
        endpoint_url = f'/samples/<sample_id>/{cls.name()}'
        endpoint_name = f'post_{cls.name()}'
        view_function = cls.receive_upload
        router.add_url_rule(endpoint_url,
                            endpoint_name,
                            view_function,
                            methods=['POST'])

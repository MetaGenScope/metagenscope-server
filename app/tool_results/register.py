"""Base module for Tool Results."""

from uuid import UUID

from flask import request

from app.api.endpoint_response import EndpointResponse
from app.api.utils import handle_mongo_lookup
from app.display_modules.conductor import DisplayModuleConductor
from app.samples.sample_models import Sample
from app.users.user_models import User
from app.users.user_helpers import authenticate


def receive_upload(cls, resp, sample_id):
    """Define handler for receiving uploads of analysis tool results."""
    response = EndpointResponse()

    @handle_mongo_lookup(response, cls.__name__)
    def save_tool_result():
        """Validate and save tool result to Sample."""
        sample = Sample.objects.get(uuid=sample_id)
        # gh-21: Write actual validation:
        auth_user = User.query.filter_by(id=resp).first()
        if not auth_user:
            response.message = 'Authorization failed.'
            response.code = 403
        else:
            post_json = request.get_json()
            tool_result = cls.make_result_model(post_json)
            setattr(sample, cls.name(), tool_result)
            sample.save()
            response.success(201)
            response.data = post_json

            # Kick off middleware tasks
            DisplayModuleConductor(sample_id, cls).shake_that_baton()

        return response.json_and_code()
    return save_tool_result()


def register_api_call(cls, router):
    """Register API endpoint for this display module type."""
    endpoint_url = f'/samples/<sample_uuid>/{cls.name()}'
    endpoint_name = f'post_{cls.name()}'

    @authenticate
    def view_function(resp, sample_uuid):
        """Wrap receive_upload to provide class."""
        sample_uuid = UUID(sample_uuid)
        return receive_upload(cls, resp, sample_uuid)

    router.add_url_rule(endpoint_url,
                        endpoint_name,
                        view_function,
                        methods=['POST'])


def register_modules(modules, router):
    """Register module API endpoints."""
    for module in modules:
        register_api_call(module, router)

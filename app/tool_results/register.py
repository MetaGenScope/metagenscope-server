"""Base module for Tool Results."""

from flask import request
from flask_mongoengine.wtf import model_form

from app.extensions import mongoDB
from app.users.user_models import User
from app.samples.sample_models import Sample
from app.users.user_helpers import authenticate
from app.api.endpoint_response import EndpointResponse

@authenticate
def receive_upload(cls, resp, sample_id):
    """Define handler for receiving uploads of analysis tool results."""
    response = EndpointResponse()
    # TODO: Check Sample exists
    print(sample_id)
    # TODO: Ensure user has permission on Sample
    auth_user = User.query.filter_by(id=resp).first()
    print(auth_user)
    # TODO: Upsert data
    ModelForm = model_form(cls.result_model())  # pylint: disable=invalid-name
    post_json = request.get_json()
    tool_result = ModelForm.from_json(post_json)
    if tool_result.validate():
        tool_result.save()
        response.success()
        response.data = post_json
    return response.json_and_code()


def register_api_call(cls, router):
    """Register API endpoint for this display module type."""
    endpoint_url = f'/samples/<sample_id>/{cls.name()}'
    endpoint_name = f'post_{cls.name()}'
    view_function = lambda resp, sample_id: receive_upload(cls, resp, sample_id)
    router.add_url_rule(endpoint_url,
                        endpoint_name,
                        view_function,
                        methods=['POST'])

def register_modules(modules, router):
    """Register list of modules."""
    for module in modules:
        # Register sub-document properties on Sample
        module_name = module.name()
        result_model = module.result_model()
        result_field = mongoDB.EmbeddedDocumentField(result_model)
        setattr(Sample, module_name, result_field)

        # Register API endpoints
        register_api_call(module, router)

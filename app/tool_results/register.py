"""Base module for Tool Results."""

from uuid import UUID

from flask import request
from flask import current_app
from flask_api.exceptions import NotFound, ParseError, PermissionDenied
from mongoengine.errors import ValidationError, DoesNotExist
from sqlalchemy.orm.exc import NoResultFound

from app.display_modules.conductor import DisplayModuleConductor
from app.samples.sample_models import Sample
from app.users.user_models import User
from app.users.user_helpers import authenticate


def receive_upload(cls, resp, sample_uuid):
    """Define handler for receiving uploads of analysis tool results."""
    try:
        uuid = UUID(sample_uuid)
        sample = Sample.objects.get(uuid=uuid)
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')

    # gh-21: Write actual validation:
    try:
        auth_user = User.query.filter_by(id=resp).one()
        print(auth_user)
    except NoResultFound:
        raise PermissionDenied('Authorization failed.')

    try:
        post_json = request.get_json()
        tool_result = cls.make_result_model(post_json)
        setattr(sample, cls.name(), tool_result)
        sample.save()
    except ValidationError as validation_error:
        raise ParseError(str(validation_error))

    # Kick off middleware tasks
    try:
        DisplayModuleConductor(sample_uuid, cls).shake_that_baton()
    except Exception as exc:  # pylint: disable=broad-except
        current_app.logger.exception('Exception while coordinating display modules.')
        current_app.logger.exception(exc)

    return post_json, 201


def register_api_call(cls, router):
    """Register API endpoint for this display module type."""
    endpoint_url = f'/samples/<sample_uuid>/{cls.name()}'
    endpoint_name = f'post_{cls.name()}'

    @authenticate
    def view_function(resp, sample_uuid):
        """Wrap receive_upload to provide class."""
        return receive_upload(cls, resp, sample_uuid)

    router.add_url_rule(endpoint_url,
                        endpoint_name,
                        view_function,
                        methods=['POST'])


def register_modules(modules, router):
    """Register module API endpoints."""
    for module in modules:
        register_api_call(module, router)

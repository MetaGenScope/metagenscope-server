"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, request
from mongoengine.errors import ValidationError
from sqlalchemy.exc import IntegrityError

from app.api.endpoint_response import EndpointResponse
from app.api.utils import handle_mongo_lookup
from app.extensions import db
from app.samples.sample_models import Sample, sample_schema
from app.users.user_helpers import authenticate


samples_blueprint = Blueprint('samples', __name__)    # pylint: disable=invalid-name


@samples_blueprint.route('/samples', methods=['POST'])
@authenticate
# pylint: disable=unused-argument
def add_sample_group(resp):
    """Add sample."""
    response = EndpointResponse()
    post_data = request.get_json()
    if not post_data:
        response.message = 'Invalid Sample creation payload.'
        response.code = 400
        return response.json_and_code()
    try:
        # Get params
        sample_name = post_data.get('name')
        # Create Sample
        sample = Sample(name=sample_name).save()
        db.session.commit()
        # Update respone
        response.success(201)
        response.data = sample_schema.dump(sample).data
    except ValidationError as validation_error:
        # Most likely a duplicate Sample Name error
        response.message = f'Validation error: {str(validation_error)}'
        response.code = 400
    except IntegrityError as integrity_error:
        print(integrity_error)
        db.session.rollback()
        response.message = f'Integrity error: {str(integrity_error)}'
        response.code = 400
    return response.json_and_code()


@samples_blueprint.route('/samples/<sample_uuid>', methods=['GET'])
def get_single_sample(sample_uuid):
    """Get single sample details."""
    response = EndpointResponse()

    @handle_mongo_lookup(response, 'Sample')
    def fetch_sample():
        """Perform sample lookup and formatting."""
        uuid = UUID(sample_uuid)
        sample = Sample.objects.get(uuid=uuid)
        response.success()
        response.data = sample_schema.dump(sample).data
        return response.json_and_code()

    return fetch_sample()

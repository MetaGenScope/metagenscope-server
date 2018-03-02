"""Organization API endpoint definitions."""

from flask import Blueprint

from app.api.endpoint_response import EndpointResponse
from app.api.utils import slug2uuid, handle_mongo_lookup
from app.samples.sample_models import Sample, sample_schema


samples_blueprint = Blueprint('samples', __name__)    # pylint: disable=invalid-name


@samples_blueprint.route('/samples/<sample_slug>', methods=['GET'])
def get_single_sample(sample_slug):
    """Get single sample details."""
    response = EndpointResponse()

    @handle_mongo_lookup(response, 'Sample')
    def fetch_sample():
        """Perform sample lookup and formatting."""
        sample_id = slug2uuid(sample_slug)
        sample = Sample.objects(uuid=sample_id)[0]
        response.success()
        response.data = sample_schema.dump(sample).data
        return response.json_and_code()

    return fetch_sample()

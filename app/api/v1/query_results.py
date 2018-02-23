"""Query Result API endpoint definitions."""

from flask import Blueprint
from mongoengine.errors import ValidationError
from app.endpoint_response import EndpointResponse
from app.query_results.query_result_models import QueryResultMeta


# pylint: disable=invalid-name
query_results_blueprint = Blueprint('query_results', __name__)


@query_results_blueprint.route('/query_results/<result_id>', methods=['GET'])
def get_single_result(result_id):
    """Get single query result."""
    response = EndpointResponse()
    try:
        query_result = QueryResultMeta.objects(id=result_id)[0]
        response.success()
        response.data = {
            'id': str(query_result.id),
            'sample_group_id': query_result.sample_group_id,
            'result_types': query_result.result_types,
        }
    except IndexError:
        response.message = 'Query Result does not exist.'
    except ValidationError as validation_error:
        response.message = f'{validation_error}'
        response.code = 400
    return response.json_and_code()





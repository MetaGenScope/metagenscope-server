"""Query Result API endpoint definitions."""

from flask import Blueprint

from app.api.endpoint_response import EndpointResponse
from app.api.utils import handle_mongo_lookup
from app.query_results.query_result_models import QueryResultMeta


query_results_blueprint = Blueprint('query_results', __name__)  # pylint: disable=invalid-name


@query_results_blueprint.route('/query_results/<result_uuid>', methods=['GET'])
def get_single_result(result_uuid):
    """Get single query result."""
    response = EndpointResponse()

    @handle_mongo_lookup(response, 'Query Result')
    def fetch_result():
        """Perform database lookup."""
        query_result = QueryResultMeta.objects.get(uuid=result_uuid)
        response.success()
        response.data = {
            'id': str(query_result.id),
            'sample_group_id': query_result.sample_group_id,
            'result_types': query_result.result_types,
        }
        return response.json_and_code()

    return fetch_result()

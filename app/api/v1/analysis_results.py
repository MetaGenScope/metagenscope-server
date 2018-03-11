"""Analysis Result API endpoint definitions."""

from flask import Blueprint

from app.api.endpoint_response import EndpointResponse
from app.api.utils import handle_mongo_lookup
from app.analysis_results.analysis_result_models import AnalysisResultMeta


analysis_results_blueprint = Blueprint('analysis_results', __name__)  # pylint: disable=invalid-name


@analysis_results_blueprint.route('/analysis_results/<result_uuid>', methods=['GET'])
def get_single_result(result_uuid):
    """Get single analysis result."""
    response = EndpointResponse()

    @handle_mongo_lookup(response, 'Analysis Result')
    def fetch_result():
        """Perform database lookup."""
        analysis_result = AnalysisResultMeta.objects.get(uuid=result_uuid)
        response.success()
        response.data = {
            'id': str(analysis_result.id),
            'sample_group_id': analysis_result.sample_group_id,
            'result_types': analysis_result.result_types,
        }
        return response.json_and_code()

    return fetch_result()

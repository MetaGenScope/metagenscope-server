"""Analysis Result API endpoint definitions."""

from flask import Blueprint

from app.api.utils import handle_mongo_lookup
from app.analysis_results.analysis_result_models import AnalysisResultMeta


analysis_results_blueprint = Blueprint('analysis_results', __name__)  # pylint: disable=invalid-name


@analysis_results_blueprint.route('/analysis_results/<result_uuid>', methods=['GET'])
def get_single_result(result_uuid):
    """Get single analysis result."""

    @handle_mongo_lookup('Analysis Result')
    def fetch_result():
        """Perform database lookup."""
        analysis_result = AnalysisResultMeta.objects.get(uuid=result_uuid)
        result = {
            'id': str(analysis_result.id),
            'sample_group_id': analysis_result.sample_group_id,
            'result_types': analysis_result.result_types,
        }
        return result, 200

    return fetch_result()

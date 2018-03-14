"""Analysis Result API endpoint definitions."""

from uuid import UUID

from flask import Blueprint
from flask_api.exceptions import NotFound, ParseError
from mongoengine import DoesNotExist

from app.analysis_results.analysis_result_models import AnalysisResultMeta


analysis_results_blueprint = Blueprint('analysis_results', __name__)  # pylint: disable=invalid-name


@analysis_results_blueprint.route('/analysis_results/<result_uuid>', methods=['GET'])
def get_single_result(result_uuid):
    """Get single analysis result."""
    try:
        uuid = UUID(result_uuid)
        analysis_result = AnalysisResultMeta.objects.get(uuid=uuid)
        result = {
            'id': str(analysis_result.id),
            'sample_group_id': analysis_result.sample_group_id,
            'result_types': analysis_result.result_types,
        }
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')

"""Handle API registration of display modules."""

from uuid import UUID

from flask_api.exceptions import NotFound, ParseError
from mongoengine.errors import DoesNotExist

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.api.exceptions import InvalidRequest

from .utils import jsonify


def get_result(display_module, result_uuid):
    """Define handler for API requests that defers to display module type."""
    try:
        uuid = UUID(result_uuid)
        analysis_result = AnalysisResultMeta.objects.get(uuid=uuid)
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')

    if display_module.name() not in analysis_result:
        raise InvalidRequest(f'{display_module.name()} is not in this AnalysisResult.')

    module_results = getattr(analysis_result, display_module.name()).fetch()
    result = display_module.get_data(module_results)
    for transmission_hook in display_module.transmission_hooks():
        result = transmission_hook(result)

    # Conversion to dict is necessary to avoid object not callable TypeError
    result_dict = jsonify(result)
    return result_dict, 200


def register_display_module(display_module, router):
    """Register API endpoint for this display module type."""
    endpoint_url = f'/analysis_results/<result_uuid>/{display_module.name()}'
    endpoint_name = f'get_{display_module.name()}'

    def view_function(result_uuid):
        """Wrap get_result to provide class."""
        return get_result(display_module, result_uuid)

    router.add_url_rule(endpoint_url,
                        endpoint_name,
                        view_function,
                        methods=['GET'])

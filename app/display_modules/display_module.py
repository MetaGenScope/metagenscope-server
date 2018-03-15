"""Base display module type."""

import json
from uuid import UUID

from flask_api.exceptions import NotFound, ParseError
from mongoengine.errors import DoesNotExist

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.api.exceptions import InvalidRequest
from app.extensions import mongoDB


class DisplayModule:
    """Base display module type."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        raise NotImplementedError()

    @classmethod
    def get_result_model(cls):
        """Return data model for display module type."""
        raise NotImplementedError()

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for display module type."""
        raise NotImplementedError()

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have for this task to run."""
        raise NotImplementedError()

    @classmethod
    def is_dependent_on_tool(cls, tool_result_cls):
        """Return True if this display module is dependent on a given Tool Result type."""
        required_tools = cls.required_tool_results()
        return tool_result_cls in required_tools

    @classmethod
    def get_data(cls, my_query_result):
        """Transform my_query_result to data."""
        return my_query_result

    @classmethod
    def api_call(cls, result_uuid):
        """Define handler for API requests that defers to display module type."""
        try:
            uuid = UUID(result_uuid)
            query_result = AnalysisResultMeta.objects.get(uuid=uuid)
        except ValueError:
            raise ParseError('Invalid UUID provided.')
        except DoesNotExist:
            raise NotFound('Analysis Result does not exist.')

        if cls.name() not in query_result:
            raise InvalidRequest(f'{cls.name()} is not in this AnalysisResult.')

        module_results = getattr(query_result, cls.name())
        result = cls.get_data(module_results)
        # Conversion to dict is necessary to avoid object not callable TypeError
        result_dict = json.loads(result.to_json())
        return result_dict, 200

    @classmethod
    def register_api_call(cls, router):
        """Register API endpoint for this display module type."""
        endpoint_url = f'/analysis_results/<result_uuid>/{cls.name()}'
        endpoint_name = f'get_{cls.name()}'
        view_function = cls.api_call
        router.add_url_rule(endpoint_url,
                            endpoint_name,
                            view_function,
                            methods=['GET'])

    @classmethod
    def get_analysis_result_wrapper(cls):
        """Create wrapper for analysis result data field."""
        module_result_model = cls.get_result_model()
        mongo_field = mongoDB.EmbeddedDocumentField(module_result_model)
        # Convert snake-cased name() to upper camel-case class name
        words = cls.name().split('_')
        words = [word[0].upper() + word[1:] for word in words]
        class_name = ''.join(words) + 'ResultWrapper'
        # Create wrapper class
        return type(class_name,
                    (AnalysisResultWrapper,),
                    {'data': mongo_field})

"""Base display module type."""

from uuid import UUID

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.api.endpoint_response import EndpointResponse
from app.api.utils import handle_mongo_lookup
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
    def get_result_wrangler(cls):
        """Return middleware wrangler for display module type."""
        raise NotImplementedError()

    @classmethod
    def get_data(cls, my_query_result):
        """Transform my_query_result to data."""
        return my_query_result

    @classmethod
    def api_call(cls, result_uuid):
        """Define handler for API requests that defers to display module type."""
        response = EndpointResponse()

        @handle_mongo_lookup(response, 'Analysis Result')
        def fetch_data():
            """Perform Analysis Result lookup and formatting."""
            uuid = UUID(result_uuid)
            query_result = AnalysisResultMeta.objects.get(uuid=uuid)
            if cls.name() not in query_result:
                msg = '{} is not in this AnalysisResult.'.format(cls.name())
                response.message = msg
            elif query_result[cls.name()]['status'] != 'S':
                response.message = 'Analysis Result has not finished processing.'
            else:
                response.success()
                response.data = cls.get_data(query_result[cls.name()])
            return response.json_and_code()

        return fetch_data()

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

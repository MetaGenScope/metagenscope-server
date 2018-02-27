"""Base display module type."""

from mongoengine.errors import ValidationError

from app.query_results.query_result_models import QueryResultMeta, QueryResultWrapper
from app.api.v1.endpoint_response import EndpointResponse


class DisplayModule:
    """Base display module type."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        raise NotImplementedError()

    @classmethod
    def get_data(cls, my_query_result):
        """Transform my_query_result to data."""
        return my_query_result

    @classmethod
    def api_call(cls, result_id):
        """Define handler for API requests that defers to display module type."""
        response = EndpointResponse()
        try:
            query_result = QueryResultMeta.objects(id=result_id)[0]
            if cls.name() not in query_result:
                msg = '{} is not in this QueryResult.'.format(cls.name())
                response.message = msg
            elif query_result[cls.name()]['status'] != 'S':
                response.message = 'Query Result has not finished processing.'
            else:
                response.success()
                response.data = cls.get_data(query_result[cls.name()])
        except IndexError:
            response.message = 'Query Result does not exist.'
        except ValidationError as validation_error:
            response.message = f'{validation_error}'
            response.code = 400
        return response.json_and_code()

    @classmethod
    def register_api_call(cls, router):
        """Register API endpoint for this display module type."""
        endpt_url = '/query_results/<result_id>/{}'.format(cls.name())
        router.add_url_rule(endpt_url,
                            cls.api_call,
                            methods=['GET'])

    @classmethod
    def get_mongodb_embedded_docs(cls):
        """Return sub-document types for display module type."""
        raise NotImplementedError()

    @classmethod
    def get_query_result_wrapper(cls):
        """Create wrapper for query result field."""
        mongo_field = cls.get_query_result_wrapper_field()
        words = cls.name().split('_')
        words = [word[0].upper() + word[:1] for word in words]
        class_name = ''.join(words) + 'ResultWrapper'
        out = type(class_name,
                   (QueryResultWrapper,),
                   {'data': mongo_field})
        return out

    @classmethod
    def get_query_result_wrapper_field(cls):
        """Return status wrapper for display module type."""
        raise NotImplementedError()

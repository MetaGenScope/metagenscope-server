from mongoengine.errors import ValidationError
from app.query_results.query_result_models import QueryResultMeta, QueryResultWrapper
from app.endpoint_response import EndpointResponse


class DisplayModule:

    @classmethod
    def name(ctype):
        raise NotImplementedError()

    @classmethod
    def get_data(ctype, my_query_result):
        raise NotImplementedError()

    @classmethod
    def api_call(ctype, result_id):
        response = EndpointResponse()
        try:
            query_result = QueryResultMeta.objects(id=result_id)[0]
            if ctype.name() not in query_result:
                msg = '{} is not in this QueryResult.'.format(ctype.name())
                response.message = msg
            elif query_result[ctype.name()]['status'] != 'S':
                response.message = 'Query Result has not finished processing.'
            else:
                response.success()
                response.data = ctype.get_data(query_result[ctype.name()])
        except IndexError:
            response.message = 'Query Result does not exist.'
        except ValidationError as validation_error:
            response.message = f'{validation_error}'
            response.code = 400
        return response.json_and_code()

    @classmethod
    def register_api_call(ctype, router):
        endpt_url = '/query_results/<result_id>/{}'.format(ctype.name())
        router.add_url_rule(endpt_url,
                            ctype.api_call,
                            methods=['GET'])

    @classmethod
    def get_mongodb_embedded_docs(ctype):
        raise NotImplementedError()

    @classmethod
    def get_query_result_wrapper(ctype):
        mongoField = ctype.get_query_result_wrapper_field()
        words = ctype.name().split('_')
        words = [word[0].upper() + word[:1] for word in words]
        className = ''.join(words) + 'ResultWrapper'
        out = type(className,
                    (QueryResultWrapper,),
                    {'data': mongoField})
        return out

    @classmethod
    def get_query_result_wrapper_field(ctype):
        raise NotImplementedError()

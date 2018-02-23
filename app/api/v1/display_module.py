from mongoengine.errors import ValidationError
from app.query_results.query_result_models import QueryResultMeta, QueryResultWrapper
from app.endpoint_response import EndpointResponse


class DisplayModule:

    def name(self):
        raise NotImplementedError()

    def get_data(self, my_query_result):
        raise NotImplementedError()

    def api_call(self, result_id):
        response = EndpointResponse()
        try:
            query_result = QueryResultMeta.objects(id=result_id)
            if self.name() not in query_result:
                msg = '{} is not in this QueryResult.'.format(self.name())
                response.message = msg
            elif query_result[self.name()]['status'] != 'S':
                response.message = 'Query Result has not finished processing.'
            else:
                response.success()
                response.data = self.get_data(query_result[self.name()])
        except IndexError:
            pass
        except ValidationError as validation_error:
            response.message = f'{validation_error}'
            response.code = 400
        return response.json_and_code()

    def register_api_call(self, router):
        endpt_url = '/query_results/<result_id>/{}'.format(self.name())
        router.add_url_rule(endpt_url,
                            self.api_call,
                            methods=['GET'])

    def get_mongodb_embedded_docs(self):
        raise NotImplementedError()

    def get_query_result_wrapper(self):
        mongoField = self.get_query_result_wrapper_field()
        words = self.name().split('_')
        words = [word[0].upper() + word[:1] for word in words]
        className = ''.join(words) + 'ResultWrapper'
        out = type(className,
                    (QueryResultWrapper,),
                    {'data': mongoField})
        return out

    def get_query_result_wrapper_field(self):
        raise NotImplementedError()

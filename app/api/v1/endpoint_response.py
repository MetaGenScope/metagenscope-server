from flask import jsonify


class EndpointResponse:

    def __init__(self):
        self.status = 'fail'
        self.code = 404
        self.message = ''
        self.data = None

    def success(self):
        self.status = 'success'
        self.code = 200

    def json_and_code(self):
        return self.json(), self.code

    def json(self):
        obj = {
            'status': self.status,
        }
        if self.status == 'success':
            obj['data'] = self.data
        else:
            obj['message'] = self.message
        return jsonify(obj)

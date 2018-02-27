"""Simplify Flask endpoint reponses."""

from flask import jsonify


class EndpointResponse:
    """Object wrapping json resonse generation for API endpoints."""

    def __init__(self):
        """Initialize EndpointResponse."""
        self.status = 'fail'
        self.code = 404
        self.message = ''
        self.data = None

    def success(self):
        """Set response as successful."""
        self.status = 'success'
        self.code = 200

    def json_and_code(self):
        """Return EndpointResponse as Flask-format response."""
        return self.json(), self.code

    def json(self):
        """Build JSON from response data."""
        obj = {
            'status': self.status,
        }
        if self.status == 'success':
            obj['data'] = self.data
        else:
            obj['message'] = self.message
        return jsonify(obj)

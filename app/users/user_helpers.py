"""Helper methods related to User model."""

from functools import wraps

from flask import request

from app.api.endpoint_response import EndpointResponse
from app.users.user_models import User


def authenticate(f):  # pylint: disable=invalid-name
    """Decorate API route calls requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Wrap function f."""
        response = EndpointResponse()
        response.code = 401
        response.message = 'Something went wrong. Please contact us.'

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response.message = 'Provide a valid auth token.'
            return response.json_and_code()
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response.message = resp
            return response.json_and_code()
        user = User.query.filter_by(id=resp).first()
        if not user or not user.active:
            return response.json_and_code()
        return f(resp, *args, **kwargs)
    return decorated_function

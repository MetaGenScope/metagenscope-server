"""Helper methods related to User model."""

from functools import wraps

from flask import request, jsonify

from app.users.user_models import User


# pylint: disable=invalid-name
def authenticate(f):
    """Decorate API route calls requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Wrap function f."""
        response_object = {
            'status': 'error',
            'message': 'Something went wrong. Please contact us.'
        }
        unauthorized_code = 401
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response_object['message'] = 'Provide a valid auth token.'
            return jsonify(response_object), unauthorized_code
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), unauthorized_code
        user = User.query.filter_by(id=resp).first()
        if not user or not user.active:
            return jsonify(response_object), unauthorized_code
        return f(resp, *args, **kwargs)
    return decorated_function

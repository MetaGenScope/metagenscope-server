"""Helper methods related to User model."""

import base64

from functools import wraps
from uuid import UUID

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
        code = 401
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response_object['message'] = 'Provide a valid auth token.'
            code = 403
            return jsonify(response_object), code
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), code
        user = User.query.filter_by(id=resp).first()
        if not user or not user.active:
            return jsonify(response_object), code
        return f(resp, *args, **kwargs)
    return decorated_function


# Based on https://stackoverflow.com/a/12270917
def uuid2slug(uuidstring):
    """Convert UUID string to URL-safe base64 encoded slug."""
    base64UUID = base64.urlsafe_b64encode(UUID(uuidstring).bytes)
    return base64UUID.decode('utf-8').rstrip('=\n').replace('/', '_')


def slug2uuid(slug):
    """Convert URL-safe base64 encoded slug to UUID string."""
    return str(UUID(bytes=base64.urlsafe_b64decode((slug + '==').replace('_', '/'))))

"""API Exceptions."""

from flask_api.exceptions import APIException


class InvalidRequest(APIException):
    """Exception for invalid requests."""

    status_code = 400
    detail = 'Request is invalid.'


class InternalError(APIException):
    """Exception for unexpected internal errors."""

    status_code = 500
    detail = 'MetaGenScope encountered an unexpected internal errors.'

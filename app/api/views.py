"""API endpoint definitions."""


from flask import Blueprint, jsonify


# pylint: disable=invalid-name
users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    """Respond to ping."""
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

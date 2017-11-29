"""Ping API endpoint definitions."""


from flask import Blueprint, jsonify


# pylint: disable=invalid-name
ping_blueprint = Blueprint('ping', __name__)


@ping_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    """Respond to ping."""
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

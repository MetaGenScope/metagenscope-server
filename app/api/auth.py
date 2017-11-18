"""Authentication API endpoint definitions."""

from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from app.extensions import db, bcrypt
from app.api.models import User
from app.api.utils import authenticate


# pylint: disable=invalid-name
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    """Register user."""
    # Get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # Check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)).first()
        if not user:
            # Add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            # Generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return jsonify(response_object), 201
        response_object = {
            'status': 'error',
            'message': 'Sorry. That user already exists.'
        }
        return jsonify(response_object), 400
    # Handler errors
    except (exc.IntegrityError, ValueError) as e:
        print(e)
        db.session.rollback()
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    """Log user in."""
    # Get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # Fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return jsonify(response_object), 200
        response_object = {
            'status': 'error',
            'message': 'User does not exist.'
        }
        return jsonify(response_object), 404
    # pylint: disable=broad-except
    except Exception as e:
        print(e)
        response_object = {
            'status': 'error',
            'message': 'Try again.'
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp):
    """Log user out."""
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200


@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    """Get user status."""
    user = User.query.filter_by(id=resp).first()
    response_object = {
        'status': 'success',
        'data': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'active': user.active,
            'created_at': user.created_at
        }
    }
    return jsonify(response_object), 200

"""Authentication API endpoint definitions."""

from flask import Blueprint, current_app, request
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.api.endpoint_response import EndpointResponse
from app.extensions import db, bcrypt
from app.users.user_models import User
from app.users.user_helpers import authenticate


# pylint: disable=invalid-name
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    """Register user."""
    response = EndpointResponse()
    # Get post data
    post_data = request.get_json()
    if not post_data:
        response.code = 400
        response.message = 'Invalid registration payload.'
        return response.json_and_code()
    try:
        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        # Check for existing user
        user = User.query.filter(or_(User.username == username,
                                     User.email == email)).first()
        if not user:
            # Add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password,
            )
            db.session.add(new_user)
            db.session.commit()
            # Generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response.success(201)
            response.data = {'auth_token': auth_token.decode()}
        else:
            response.code = 400
            response.message = 'Sorry. That user already exists.'
    # Handler errors
    except (IntegrityError, ValueError):
        current_app.logger.exception('There was a problem with registration.')
        db.session.rollback()
        response.code = 400
        response.message = 'Invalid payload.'
    return response.json_and_code()


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    """Log user in."""
    response = EndpointResponse()
    # Get post data
    post_data = request.get_json()
    if not post_data:
        response.code = 400
        response.message = 'Invalid login payload.'
        return response.json_and_code()
    email = post_data.get('email')
    password = post_data.get('password')
    # Fetch the user data
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
            response.success(200)
            response.data = {'auth_token': auth_token.decode()}
            return response.json_and_code()
    response.code = 404
    response.message = 'User does not exist.'
    return response.json_and_code()


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp):  # pylint: disable=unused-argument
    """Log user out."""
    response = EndpointResponse()
    response.success(200)
    return response.json_and_code()


@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    """Get user status."""
    response = EndpointResponse()
    user = User.query.filter_by(id=resp).first()
    response.success(200)
    response.data = {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'active': user.active,
        'created_at': user.created_at
    }
    return response.json_and_code()

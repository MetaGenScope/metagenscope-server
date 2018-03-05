"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from app.api.constants import PAGE_SIZE
from app.extensions import db
from app.organizations.organization_models import Organization, organization_schema
from app.users.user_models import User, user_schema
from app.users.user_helpers import authenticate
from app.sample_groups.sample_group_models import sample_group_schema


organizations_blueprint = Blueprint('organizations', __name__)  # pylint: disable=invalid-name


@organizations_blueprint.route('/organizations', methods=['POST'])
@authenticate
# pylint: disable=unused-argument
def add_organization(resp):
    """Add organization."""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    name = post_data.get('name')
    admin_email = post_data.get('admin_email')
    try:
        organization = Organization.query.filter_by(name=name).first()
        if not organization:
            db.session.add(Organization(name=name, admin_email=admin_email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{name} was added!'
            }
            return jsonify(response_object), 201
        response_object = {
            'status': 'fail',
            'message': 'Sorry. That name already exists.'
        }
        return jsonify(response_object), 400
    except exc.IntegrityError as integrity_error:
        print(integrity_error)
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@organizations_blueprint.route('/organizations/<organization_uuid>', methods=['GET'])
def get_single_organization(organization_uuid):
    """Get single organization details."""
    response_object = {
        'status': 'fail',
        'message': 'Organization does not exist'
    }
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': organization_schema.dump(organization).data,
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@organizations_blueprint.route('/organizations/<organization_uuid>/users', methods=['GET'])
def get_organization_users(organization_uuid):
    """Get single organization's users."""
    response_object = {
        'status': 'fail',
        'message': 'Organization does not exist'
    }
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            return jsonify(response_object), 404
        users = user_schema.dump(organization.users, many=True).data
        response_object = {
            'status': 'success',
            'data': users,
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@organizations_blueprint.route('/organizations/<organization_uuid>/users', methods=['POST'])
@authenticate
def add_organization_user(resp, organization_uuid):     # pylint: disable=too-many-return-statements
    """Add user to organization."""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_object), 400
    user_id = post_data.get('user_id')
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            response_object['message'] = 'Organization does not exist'
            return jsonify(response_object), 404

        auth_user = User.query.filter_by(id=resp).first()
        if not auth_user or auth_user not in organization.admin_users:
            response_object = {
                'status': 'fail',
                'message': 'You do not have permission to perform that action.'
            }
            return jsonify(response_object), 403
        user = User.query.filter_by(id=user_id).first()
        if not user:
            response_object['message'] = 'User does not exist'
            return jsonify(response_object), 404
        try:
            organization.users.append(user)
            response_object = {
                'status': 'success',
                'message': f'${user.username} added to ${organization.name}'
            }
            return jsonify(response_object), 200
        except Exception as integrity_error:      # pylint: disable=broad-except
            response_object['message'] = f'Exception: ${str(integrity_error)}'
            return jsonify(response_object), 500
    except ValueError:
        return jsonify(response_object), 404


@organizations_blueprint.route('/organizations/<organization_uuid>/sample_groups',
                               methods=['GET'])
@organizations_blueprint.route('/organizations/<organization_uuid>/sample_groups/<int:page>',
                               methods=['GET'])
def get_organization_sample_groups(organization_uuid, page=1):
    """Get single organization's sample groups."""
    response_object = {
        'status': 'fail',
        'message': 'Organization does not exist'
    }
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            return jsonify(response_object), 404
        sample_groups = organization.sample_groups.paginate(page, PAGE_SIZE, False).items
        response_object = {
            'status': 'success',
            'data': sample_group_schema.dump(sample_groups, many=True).data,
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@organizations_blueprint.route('/organizations', methods=['GET'])
def get_all_organizations():
    """Get all organizations."""
    organizations = Organization.query.all()
    response_object = {
        'status': 'success',
        'data': organization_schema.dump(organizations, many=True).data,
    }
    return jsonify(response_object), 200

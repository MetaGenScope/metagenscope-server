"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from sqlalchemy import exc

from app.api.constants import PAGE_SIZE
from app.api.endpoint_response import EndpointResponse
from app.extensions import db
from app.organizations.organization_models import Organization, organization_schema
from app.users.user_models import User, user_schema
from app.users.user_helpers import authenticate
from app.sample_groups.sample_group_models import sample_group_schema


organizations_blueprint = Blueprint('organizations', __name__)  # pylint: disable=invalid-name


@organizations_blueprint.route('/organizations', methods=['POST'])
@authenticate
def add_organization(resp):  # pylint: disable=unused-argument
    """Add organization."""
    response = EndpointResponse()
    post_data = request.get_json()
    if not post_data:
        response.code = 400
        response.message = 'Invalid organization payload.'
        return response.json_and_code()
    try:
        name = post_data.get('name')
        admin_email = post_data.get('admin_email')
        organization = Organization.query.filter_by(name=name).first()
        if not organization:
            db.session.add(Organization(name=name, admin_email=admin_email))
            db.session.commit()
            response.success(201)
            response.data = {'message': f'{name} was added!'}
        else:
            response.status = 400
            response.message = 'Sorry. That name already exists.'
    except exc.IntegrityError:
        current_app.logger.exception('There was a problem adding an organization.')
        db.session.rollback()
        response.code = 400
        response.message = 'Invalid organization payload.'
    return response.json_and_code()


@organizations_blueprint.route('/organizations/<organization_uuid>', methods=['GET'])
def get_single_organization(organization_uuid):
    """Get single organization details."""
    response = EndpointResponse()
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            raise ValueError('Organization does not exist')
        response.success(200)
        response.data = organization_schema.dump(organization).data
    except ValueError as value_error:
        current_app.logger.exception('ValueError encountered.')
        response.code = 404
        response.message = str(value_error)
    return response.json_and_code()


@organizations_blueprint.route('/organizations/<organization_uuid>/users', methods=['GET'])
def get_organization_users(organization_uuid):
    """Get single organization's users."""
    response = EndpointResponse()
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            raise ValueError('Organization does not exist')
        users = user_schema.dump(organization.users, many=True).data
        response.success(200)
        response.data = users
    except ValueError as value_error:
        current_app.logger.exception('ValueError encountered.')
        response.code = 404
        response.message = str(value_error)
    return response.json_and_code()


@organizations_blueprint.route('/organizations/<organization_uuid>/users', methods=['POST'])
@authenticate
def add_organization_user(resp, organization_uuid):     # pylint: disable=too-many-return-statements
    """Add user to organization."""
    response = EndpointResponse()
    post_data = request.get_json()
    if not post_data:
        response.code = 400
        response.message = 'Invalid membership payload.'
        return response.json_and_code()
    try:
        user_id = post_data.get('user_id')
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            response.code = 404
            response.message = 'Organization does not exist'
            return response.json_and_code()

        auth_user = User.query.filter_by(id=resp).first()
        if not auth_user or auth_user not in organization.admin_users:
            response.code = 403
            response.message = 'You do not have permission to perform that action.'
            return response.json_and_code()

        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError('User does not exist')

        try:
            organization.users.append(user)
            response.success(200)
            message = f'${user.username} added to ${organization.name}'
            response.data = {'message': message}
        except Exception as integrity_error:      # pylint: disable=broad-except
            current_app.logger.exception('Exception encountered.')
            response.code = 500
            response.message = f'Exception: ${str(integrity_error)}'
    except ValueError as value_error:
        current_app.logger.exception('ValueError encountered.')
        response.code = 404
        response.message = str(value_error)
    return response.json_and_code()


@organizations_blueprint.route('/organizations/<organization_uuid>/sample_groups',
                               methods=['GET'])
@organizations_blueprint.route('/organizations/<organization_uuid>/sample_groups/<int:page>',
                               methods=['GET'])
def get_organization_sample_groups(organization_uuid, page=1):
    """Get single organization's sample groups."""
    response = EndpointResponse()
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            raise ValueError('Organization does not exist')
        sample_groups = organization.sample_groups.paginate(page, PAGE_SIZE, False).items
        response.success(200)
        response.data = sample_group_schema.dump(sample_groups, many=True).data
    except ValueError as value_error:
        response.code = 404
        response.message = str(value_error)
    return response.json_and_code()


@organizations_blueprint.route('/organizations', methods=['GET'])
def get_all_organizations():
    """Get all organizations."""
    response = EndpointResponse()
    organizations = Organization.query.all()
    response.data = organization_schema.dump(organizations, many=True).data
    response.success(200)
    return response.json_and_code()

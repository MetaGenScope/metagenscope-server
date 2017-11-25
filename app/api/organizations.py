"""Organization API endpoint definitions."""


from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from app.extensions import db
from app.api.models import Organization
from app.api.utils import authenticate


# pylint: disable=invalid-name
organizations_blueprint = Blueprint('organizations', __name__)


@organizations_blueprint.route('/organizations', methods=['POST'])
@authenticate
def add_organization():
    """Respond to ping."""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    name = post_data.get('name')
    admin_email = post_data.get('adminEmail')
    try:
        organization = Organization.query.filter_by(name=name).first()
        if not organization:
            db.session.add(Organization(name=name, adminEmail=admin_email))
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
    except exc.IntegrityError as e:
        print(e)
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

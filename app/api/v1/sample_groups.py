"""Sample Group API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.api.endpoint_response import EndpointResponse
from app.extensions import db
from app.sample_groups.sample_group_models import SampleGroup, sample_group_schema
from app.samples.sample_models import Sample
from app.users.user_helpers import authenticate


# pylint: disable=invalid-name
sample_groups_blueprint = Blueprint('sample_groups', __name__)


@sample_groups_blueprint.route('/sample_groups', methods=['POST'])
@authenticate
# pylint: disable=unused-argument
def add_sample_group(resp):
    """Add sample group."""
    response = EndpointResponse()
    post_data = request.get_json()
    if not post_data:
        response.message = 'Invalid Sample Group creation payload.'
        response.code = 400
        return response.json_and_code()
    try:
        name = post_data.get('name')
        sample_group = SampleGroup(name=name)
        db.session.add(sample_group)
        db.session.commit()
        response.success(201)
        response.data = sample_group_schema.dump(sample_group).data
    except IntegrityError as integrity_error:
        print(integrity_error)
        db.session.rollback()
        response.message = f'Integrity error: {str(integrity_error)}'
        response.code = 400
    return response.json_and_code()


@sample_groups_blueprint.route('/sample_groups/<group_uuid>', methods=['GET'])
def get_single_result(group_uuid):
    """Get single sample group model."""
    response = EndpointResponse()
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
        response.data = sample_group_schema.dump(sample_group).data
        response.success()
    except (ValueError, NoResultFound):
        response.message = 'Sample Group does not exist'
        response.code = 404
    return response.json_and_code()


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/add_samples', methods=['POST'])
@authenticate
def add_samples_to_group(group_uuid, resp):
    """Get single sample group model."""
    response = EndpointResponse()
    post_data = request.get_json()
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()

    except (ValueError, NoResultFound):
        response.message = 'Sample Group does not exist'
        response.code = 404
        return response.json_and_code()

    try:
        sample_uuids = [UUID(uuid) for uuid in post_data.get('sample_uuids')]
        for sample_uuid in sample_uuids:
            sample = Sample.objects.get(uuid=sample_uuid)
            sample_group.sample_ids.append(sample.uuid)
        db.session.commit()
        response.data = sample_group_schema.dump(sample_group).data
        response.success()
    except NoResultFound:
        response.message = f'Sample UUID \'{sample_uuid}\' does not exist'
        response.code = 400
        return response.json_and_code()

    return response.json_and_code()

"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError
from mongoengine.errors import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.api.exceptions import InvalidRequest, InternalError
from app.api.utils import handle_mongo_lookup
from app.extensions import db
from app.samples.sample_models import Sample, sample_schema
from app.sample_groups.sample_group_models import SampleGroup
from app.users.user_helpers import authenticate


samples_blueprint = Blueprint('samples', __name__)    # pylint: disable=invalid-name


@samples_blueprint.route('/samples', methods=['POST'])
@authenticate
# pylint: disable=unused-argument
def add_sample(resp):
    """Add sample."""
    try:
        post_data = request.get_json()
        sample_group_uuid = post_data['sample_group_uuid']
        sample_name = post_data['name']
    except TypeError:
        raise ParseError('Missing Sample creation payload.')
    except KeyError:
        raise ParseError('Invalid Sample creation payload.')

    try:
        sample_group = SampleGroup.query.filter_by(id=sample_group_uuid).one()
    except NoResultFound:
        raise InvalidRequest('Sample Group does not exist!')

    sample = Sample.objects(name=sample_name).first()
    if sample is not None:
        raise InvalidRequest('A Sample with that name already exists.')

    try:
        sample = Sample(name=sample_name).save()
        sample_group.sample_ids.append(sample.uuid)
        db.session.commit()
        result = sample_schema.dump(sample).data
        return result, 201
    except ValidationError as validation_error:
        current_app.logger.exception('Sample could not be created.')
        raise InternalError(str(validation_error))
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample could not be added to Sample Group.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@samples_blueprint.route('/samples/<sample_uuid>', methods=['GET'])
def get_single_sample(sample_uuid):
    """Get single sample details."""

    @handle_mongo_lookup('Sample')
    def fetch_sample():
        """Perform sample lookup and formatting."""
        uuid = UUID(sample_uuid)
        sample = Sample.objects.get(uuid=uuid)
        result = sample_schema.dump(sample).data
        return result, 200

    return fetch_sample()

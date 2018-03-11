"""Sample Group API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, jsonify

from app.sample_groups.sample_group_models import SampleGroup, sample_group_schema


# pylint: disable=invalid-name
sample_groups_blueprint = Blueprint('sample_groups', __name__)


@sample_groups_blueprint.route('/sample_group/<group_uuid>', methods=['GET'])
def get_single_result(group_uuid):
    """Get single sample group model."""
    response_object = {
        'status': 'fail',
        'message': 'Sample Group does not exist'
    }
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        if not sample_group:
            return jsonify(response_object), 404
        data = sample_group_schema.dump(sample_group).data
        response_object = {
            'status': 'success',
            'data': data,
        }

        analysis_result = sample_group.analysis_result
        if analysis_result:
            response_object['data']['sample_group']['analysis_result_id'] = str(analysis_result.id)
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

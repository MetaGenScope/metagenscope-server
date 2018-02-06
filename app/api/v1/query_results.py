"""Query Result API endpoint definitions."""

from flask import Blueprint, jsonify
from mongoengine.errors import ValidationError

from app.query_results.query_result_models import QueryResultMeta


# pylint: disable=invalid-name
query_results_blueprint = Blueprint('query_results', __name__)


def list_get(L, i, v=None):
    """Return ith element in list L, or None (rather than throwing error)."""
    if -len(L) <= i < len(L):
        return L[i]
    return v


@query_results_blueprint.route('/query_results/<result_id>', methods=['GET'])
def get_single_result(result_id):
    """Get single query result."""
    response_object = {
        'status': 'fail',
        'message': 'Query Result does not exist.'
    }
    try:
        query_result = list_get(QueryResultMeta.objects(id=result_id), 0)
        if not query_result:
            return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': {
                'id': str(query_result.id),
                'sample_group_id': query_result.sample_group_id,
                'result_types': query_result.result_types,
            },
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@query_results_blueprint.route('/query_results/<result_id>/sample_similarity', methods=['GET'])
def get_sample_similarity(result_id):
    """Get single query result's sample similarity."""
    response_object = {
        'status': 'fail',
        'message': 'Sample Similarity does not exist for this Query Result.'
    }
    try:
        query_result = list_get(QueryResultMeta.objects(id=result_id), 0)
        if not query_result:
            response_object['message'] = 'Query Result does not exist.'
            return jsonify(response_object), 404
        if 'sample_similarity' not in query_result:
            return jsonify(response_object), 404
        if query_result['sample_similarity']['status'] != 'S':
            response_object['message'] = 'Query Result has not finished processing.'
            return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': query_result['sample_similarity']
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
    except ValidationError as validation_error:
        response_object['message'] = f'{validation_error}'
        return jsonify(response_object), 404


@query_results_blueprint.route('/query_results/<result_id>/taxon_abundance', methods=['GET'])
def get_taxon_abundance(result_id):
    """Get single query result's taxon abundance."""
    response_object = {
        'status': 'fail',
        'message': 'Sample Similarity does not exist for this Query Result.'
    }
    try:
        query_result = list_get(QueryResultMeta.objects(id=result_id), 0)
        if not query_result:
            response_object['message'] = 'Query Result does not exist.'
            return jsonify(response_object), 404
        if 'taxon_abundance' not in query_result:
            return jsonify(response_object), 404
        if query_result['taxon_abundance']['status'] != 'S':
            response_object['message'] = 'Query Result has not finished processing.'
            return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': query_result['taxon_abundance']
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
    except ValidationError as validation_error:
        response_object['message'] = f'{validation_error}'
        return jsonify(response_object), 404


@query_results_blueprint.route('/query_results/<result_id>/reads_classified', methods=['GET'])
def get_reads_classified(result_id):
    """Get single query result's reads classified."""
    response_object = {
        'status': 'fail',
        'message': 'Sample Similarity does not exist for this Query Result.'
    }
    try:
        query_result = list_get(QueryResultMeta.objects(id=result_id), 0)
        if not query_result:
            response_object['message'] = 'Query Result does not exist.'
            return jsonify(response_object), 404
        if 'reads_classified' not in query_result:
            return jsonify(response_object), 404
        if query_result['reads_classified']['status'] != 'S':
            response_object['message'] = 'Query Result has not finished processing.'
            return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': query_result['reads_classified']
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
    except ValidationError as validation_error:
        response_object['message'] = f'{validation_error}'
        return jsonify(response_object), 404


@query_results_blueprint.route('/query_results/<result_id>/hmp', methods=['GET'])
def get_hmp(result_id):
    """Get single query result's HMP."""
    response_object = {
        'status': 'fail',
        'message': 'Sample Similarity does not exist for this Query Result.'
    }
    try:
        query_result = list_get(QueryResultMeta.objects(id=result_id), 0)
        if not query_result:
            response_object['message'] = 'Query Result does not exist.'
            return jsonify(response_object), 404
        if 'hmp' not in query_result:
            return jsonify(response_object), 404
        if query_result['hmp']['status'] != 'S':
            response_object['message'] = 'Query Result has not finished processing.'
            return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': query_result['hmp']
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
    except ValidationError as validation_error:
        response_object['message'] = f'{validation_error}'
        return jsonify(response_object), 404

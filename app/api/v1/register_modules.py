"""Register display modules."""

from flask import Blueprint

from app.query_results.query_result_models import QueryResultMeta as QRM
from app.api.v1.display_modules import all_display_modules


query_results_blueprint = Blueprint('query_results', __name__)      # pylint: disable=invalid-name
for ctype in all_display_modules:
    ctype.register_api_call(query_results_blueprint)


MetagenomicGroupQRM = QRM.build_result_type('MetagenomicGroupQRM')  # pylint: disable=invalid-name
for ctype in all_display_modules:
    MetagenomicGroupQRM.add_property(ctype.name(),
                                     ctype.get_query_result_wrapper_field())

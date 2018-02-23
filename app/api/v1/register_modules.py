from .query_result_models import QueryResultMeta as QRM
from .display_modules import *
from flask import Blueprint


display_modules = [
    HMPModule,
    ReadsClassifiedModule,
    SampleSimilarityModule,
    TaxonAbundanceModule,
]


query_results_blueprint = Blueprint('query_results', __name__)
for ctype in display_modules:
    ctype.register_api_call(query_results_blueprint)


MetagenomicGroupQRM = QRM.build_result_type('MetagenomicGroupQRM')
for ctype in display_modules:
    MetagenomicGroupQRM.add_property(ctype.name(),
                                     ctype.get_query_result_wrapper_field())

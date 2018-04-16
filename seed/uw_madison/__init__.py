# pylint: disable=invalid-name

"""MetaGenScope seed data from UW Madison Project."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper

from .loader import load_reads_classified


reads_classified = AnalysisResultWrapper(status='S', data=load_reads_classified())

uw_analysis_result = AnalysisResultMeta(reads_classified=reads_classified)

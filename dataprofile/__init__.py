"""print or save a report of overall statistics and detailed statistics for a given dataset."""

from ._profiling import get_var_summary, get_df_profile
from .batch_cli_reports import render_reports_for_all
from .reporting import render_report, ProfileReport

__all__ = [
    'render_report',
    'ProfileReport',
    'get_var_summary',
    'get_df_profile',
    'render_reports_for_all'
]

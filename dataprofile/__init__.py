"""print or save a report of overall statistics and detailed statistics for a given dataset.
It can be used as a standalone module as well."""

from .reporting import render_report, ProfileReport
from ._profiling import get_var_summary, get_df_profile

__all__ = [
    'render_report',
    'ProfileReport',
    'get_var_summary',
    'get_df_profile',
]

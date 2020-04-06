"""print or save a report of overall statistics and detailed statistics for a given dataset.
It can be used as a standalone module as well."""

from .descriptive_report import render_report
from .collect_stats import get_var_summary, get_variable_stats

__all__ = [
    'render_report',
    'get_var_summary',
    'get_variable_stats',
]

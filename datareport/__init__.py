"""print or save a report of overall statistics and detailed statistics for a given dataset.
It can be used as a standalone module as well."""

from .descriptive_report import print_report
from .viz import plot_time_series
from .collect_stats import get_var_summary, get_variable_stats

__all__ = [
    'print_report',
    'get_var_summary',
    'get_variable_stats',
    'plot_time_series'
]

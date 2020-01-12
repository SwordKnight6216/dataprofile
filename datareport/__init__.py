"""The :mod: `dsdk.data_report` module prints a report including statistics and plots for a given dataset."""

from .descriptive_report import DataReport
from .viz import plot_time_series
from .collect_stats import get_data_type, get_variable_stats

__all__ = [
    'DataReport',
    'get_data_type',
    'get_variable_stats'
]

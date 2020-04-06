"""Compute summary statistics for various data types."""

import numpy as np
import pandas as pd

from dataprofile.config import MAX_STRING_SIZE


def base_stats(series: pd.Series) -> pd.Series:
    """
    Compute common summary statistics of a variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    length = len(series)
    count = series.count()
    distinct_count = series.nunique()

    stats = {}
    stats['count'] = length
    stats['n_missing'] = length - count
    stats['p_missing'] = f"{1 - count * 1.0 / length:.2%}"
    stats['n_unique'] = distinct_count if distinct_count else 'N/A'
    stats['p_unique'] = f"{distinct_count * 1.0 / count:.2%}" if distinct_count else 'N/A'

    return pd.Series(stats, name=series.name)


def numerical_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a numerical variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = dict(base_stats(series))
    stats['data_type'] = 'Numerical'
    stats['mean'] = series.mean()
    stats['std'] = series.std()
    stats['variance'] = series.var()
    stats['min'] = series.min()
    stats.update({"{:.0%}".format(percentile): series.dropna().quantile(percentile)
                  for percentile in [0.05, 0.25, 0.5, 0.75, 0.95]})
    stats['max'] = series.max()
    stats['range'] = stats['max'] - stats['min']
    stats['iqr'] = stats['75%'] - stats['25%']
    stats['kurtosis'] = series.kurt()
    stats['skewness'] = series.skew()
    stats['sum'] = series.sum()
    stats['mean_abs_dev'] = series.mad()
    stats['coff_of_var'] = stats['std'] / stats['mean'] if stats['mean'] else np.NaN
    stats['n_zeros'] = (stats['count'] - np.count_nonzero(series))
    stats['p_zeros'] = stats['n_zeros'] * 1.0 / stats['count']

    # round the result
    for key in stats.keys():
        try:
            stats[key] = round(stats[key], 4)
        except:
            pass

    return pd.Series(stats, name=series.name)


def datetime_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a date variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = dict(base_stats(series))
    stats['data_type'] = 'Datetime'
    stats['min'] = series.min()
    stats.update({"{:.0%}".format(percentile): series.dropna().quantile(percentile)
                  for percentile in [0.05, 0.25, 0.5, 0.75, 0.95]})
    stats['max'] = series.max()
    stats['range'] = stats['max'] - stats['min']
    day_of_week = series.dt.dayofweek
    wd_map = {0: 'n_Monday', 1: 'n_Tuesday', 2: 'n_Wednesday', 3: 'n_Thursday', 4: 'n_Friday', 5: 'n_Saturday',
              6: 'n_Sunday'}
    stats.update({v: 0 for k, v in wd_map.items()})
    day_of_week_sum = day_of_week.value_counts().rename(wd_map)
    stats.update(day_of_week_sum)

    return pd.Series(stats, name=series.name)


def categorical_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a categorical variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = dict(base_stats(series))
    aggr = series.value_counts()
    stats['data_type'] = 'Categorical'
    stats['mode'] = _str_truncate(aggr.index[0])
    stats['mode_freq'] = aggr[0]
    stats['2nd_freq_value'] = _str_truncate(aggr.index[1])
    stats['2nd_freq'] = aggr[1]
    if len(aggr) > 2:
        stats['3rd_freq_value'] = _str_truncate(aggr.index[2])
        stats['3rd_freq'] = aggr[2]

    return pd.Series(stats, name=series.name)


def binary_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a boolean variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = dict(base_stats(series))
    aggr = series.value_counts()
    stats['data_type'] = 'Binary'
    stats['value1'] = aggr.index[0]
    stats['n_value1'] = aggr[stats['value1']]
    stats['p_value1'] = f"{stats['n_value1'] / stats['count']:.2%}"
    stats['value2'] = aggr.index[1]
    stats['n_value2'] = aggr[stats['value2']]
    stats['p_value2'] = f"{stats['n_value2'] / stats['count']:.2%}"

    return pd.Series(stats, name=series.name)


def _str_truncate(s: str, max_size: int = MAX_STRING_SIZE) -> str:
    """
    Truncate a string if it is very long
    :param s:
    :param max_size:
    :return:
    """
    return f"{s[:max_size]}..." if len(s) > max_size else s

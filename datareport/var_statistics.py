"""Compute summary statistics for various data types."""

import pandas as pd
import numpy as np


def base_stats(series: pd.Series) -> pd.Series:
    """
    Compute common summary statistics of a variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    leng = len(series)
    count = series.count()
    distinct_count = series.nunique()

    stats = {}
    stats['count'] = leng
    stats['n_missing'] = leng - count
    stats['p_missing'] = f"{1 - count * 1.0 / leng:.2%}"
    stats['n_unique'] = distinct_count if distinct_count else 'N/A'
    stats['p_unique'] = f"{distinct_count * 1.0 / count:.2%}" if distinct_count else 'N/A'

    return pd.Series(stats, name=series.name)


def numerical_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a numerical variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = {}
    stats['data_type'] = 'Numerical'
    stats['mean'] = series.mean()
    stats['std'] = series.std()
    stats['variance'] = series.var()
    stats['min'] = series.min()
    stats['max'] = series.max()
    stats['range'] = stats['max'] - stats['min']
    stats.update({"{:.0%}".format(percentile): series.dropna().quantile(percentile)
                  for percentile in [0.05, 0.25, 0.5, 0.75, 0.95]})
    stats['iqr'] = stats['75%'] - stats['25%']
    stats['kurtosis'] = series.kurt()
    stats['skewness'] = series.skew()
    stats['sum'] = series.sum()
    stats['mean_abs_dev'] = series.mad()
    stats['coff_of_var'] = stats['std'] / stats['mean'] if stats['mean'] else np.NaN
    stats['n_zeros'] = (len(series) - np.count_nonzero(series))
    stats['p_zeros'] = stats['n_zeros'] * 1.0 / len(series)

    # round the result
    for key in stats.keys():
        try:
            stats[key] = round(stats[key], 4)
        except:
            pass

    return base_stats(series).append(pd.Series(stats, name=series.name))


def datetime_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a date variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = {}
    stats['data_type'] = 'Datetime'
    stats['min'] = series.min()
    stats['max'] = series.max()
    stats['range'] = stats['max'] - stats['min']

    return base_stats(series).append(pd.Series(stats, name=series.name))


def categorical_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a categorical variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = {}
    stats['data_type'] = 'Categorical'
    stats['mode'] = series.mode()[0]
    stats['mode_freq'] = series.value_counts().max()

    return base_stats(series).append(pd.Series(stats, name=series.name))


def binary_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a boolean variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = {}
    aggr = series.value_counts()
    stats['data_type'] = 'Binary'
    stats['value1'] = aggr.index[0]
    stats['n_value1'] = aggr[stats['value1']]
    stats['p_value1'] = f"{stats['n_value1']/len(series):.2%}"
    stats['value2'] = aggr.index[1]
    stats['n_value2'] = aggr[stats['value2']]
    stats['p_value2'] = f"{stats['n_value2']/len(series):.2%}"

    stats_common = base_stats(series)
    return stats_common.append(pd.Series(stats, name=series.name))


def constant_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a constant variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats_common = base_stats(series)
    return stats_common.append(pd.Series(['Constant'], index=['data_type'], name=series.name))


def unique_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a unique variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats_common = base_stats(series)
    return stats_common.append(pd.Series(['Unique'], index=['data_type'], name=series.name))


def empty_stats(series: pd.Series) -> pd.Series:
    """
    Compute summary statistics of a empty variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats_common = base_stats(series)
    return stats_common.append(pd.Series(['Empty'], index=['data_type'], name=series.name))
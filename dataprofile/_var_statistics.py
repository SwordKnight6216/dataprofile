"""Compute summary statistics for various data types."""

import numpy as np
import pandas as pd


def base_stats(series: pd.Series) -> pd.Series:
    """Compute common summary statistics of a variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    length = len(series)
    count = series.count()
    distinct_count = series.nunique()

    stats = {'count': length,
             'n_missing': length - count,
             'p_missing': f"{1 - count / length:.2%}",
             'n_unique': distinct_count if distinct_count else 'N/A',
             'p_unique': f"{distinct_count / count:.2%}" if distinct_count else 'N/A'}

    return pd.Series(stats, name=series.name)


def numerical_stats(series: pd.Series) -> pd.Series:
    """Compute summary statistics of a numerical variable.

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
    # Replace mad() with manual calculation
    stats['mean_abs_dev'] = (series - series.mean()).abs().mean()
    stats['coff_of_var'] = stats['std'] / stats['mean'] if stats['mean'] else np.NaN
    
    return pd.Series(stats, name=series.name)


def datetime_stats(series: pd.Series) -> pd.Series:
    """Compute summary statistics of a date variable.

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
    """Compute summary statistics of a categorical variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = dict(base_stats(series))
    aggr = series.value_counts()
    stats['data_type'] = 'Categorical'
    stats['mode'] = aggr.index[0]
    stats['mode_freq'] = aggr.iloc[0]  # Using iloc instead of integer indexing
    stats['2nd_freq_value'] = aggr.index[1]
    stats['2nd_freq'] = aggr.iloc[1]  # Using iloc instead of integer indexing
    if len(aggr) > 2:
        stats['3rd_freq_value'] = aggr.index[2]
        stats['3rd_freq'] = aggr.iloc[2]  # Using iloc instead of integer indexing

    return pd.Series(stats, name=series.name)


def binary_stats(series: pd.Series) -> pd.Series:
    """Compute summary statistics of a boolean variable.

    :param series: The variable to describe
    :return: descriptive statistics
    """
    stats = dict(base_stats(series))
    aggr = series.astype(str).value_counts()
    if len(aggr) > 2 and 'nan' in aggr.index:
        aggr.drop('nan', inplace=True)

    stats['data_type'] = 'Binary'
    stats['value1'] = aggr.index[0]
    stats['n_value1'] = aggr[stats['value1']]
    stats['p_value1'] = f"{stats['n_value1'] / stats['count']:.2%}"
    stats['value2'] = aggr.index[1]
    stats['n_value2'] = aggr[stats['value2']]
    stats['p_value2'] = f"{stats['n_value2'] / stats['count']:.2%}"

    return pd.Series(stats, name=series.name)

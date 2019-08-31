"""Compute summary statistics for various data types."""

import functools
import pandas as pd
import numpy as np
import re
import unicodedata
from pkg_resources import resource_stream

from dsdk.feature_types import DataType

from typing import Callable, Dict, Any, Set, Iterable

STOPWORDS_PACKAGE = 'dsdk.data_preparation.nlp.resources.text_preprocess'
STOPWORDS_PATH = 'stopwords.txt'


def get_stats_fn_by_type(data_type: DataType) -> Callable[[pd.Series], Dict[str, Any]]:
    """
    Get the corresponding function to calculate stats of data depending on its type.

    :param data_type: Type of the data.
    :return: Function to calculate the stats for the type of the given data.
    """
    if data_type == DataType.CONSTANT:
        return_fn = constant_stats
    elif data_type == DataType.CATEGORICAL:
        return_fn = categorical_stats
    elif data_type == DataType.NUMERIC:
        return_fn = numeric_stats
    elif data_type == DataType.TEXT:
        return_fn = text_stats
    elif data_type == DataType.DATETIME:
        return_fn = date_stats
    elif data_type == DataType.UNIQUE:
        return_fn = unique_stats
    return return_fn


def common_stats(series: pd.Series) -> pd.Series:
    """
    Compute common summary statistics of a variable.

    :param series: The variable to describe.
    :return: Descriptive statistics.
    """
    nrows_total = series.shape[0]
    nrows_not_missing = series.dropna().count()
    distinct_count = series.dropna().nunique()

    if nrows_not_missing == 0:
        p_unique = 0.0
    else:
        p_unique = round(distinct_count / nrows_not_missing, 4)

    stats = {
        'count': nrows_total,
        'distinct_count': distinct_count,
        'p_missing': round(1 - nrows_not_missing / nrows_total, 4),
        'n_missing': nrows_total - nrows_not_missing,
        'is_unique': distinct_count == nrows_total,
        'p_unique': p_unique,
    }
    return pd.Series(stats, name=series.name)


def add_common_stats(stats_func: Callable[[pd.Series], Dict[str, Any]]
                     ) -> Callable[[pd.Series], pd.Series]:
    """
    Add the statistics common to all feature types to the statistics for a specific feature type.

    This works like a decorator method.

    :param stats_func: A function to calculate the statistics for a specific feature type.
    :return: A function that will add on the common feature types to the specific feature types
             calculated by stats_func.
    """
    @functools.wraps(stats_func)
    def wrapper(series: pd.Series) -> pd.Series:
        stats = stats_func(series)
        stats = pd.Series(stats, name=series.name)
        stats_common = common_stats(series)
        return stats_common.append(stats)

    return wrapper


def _normalize_text(text: str) -> str:
    """
    Normalize text.

    Replace diacritics and accents with their latin equivalents and then drop any non (latin)
    alphanumeric characters.

    :param text: A string.
    :return: A string.
    """
    text_latin = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text_lower = text_latin.lower()
    pattern_alnum = re.compile(r'[^0-9a-z\s]')
    text_alphanumeric = pattern_alnum.sub('', text_lower)
    return text_alphanumeric


def _drop_stops_and_normalize(tokens_: Iterable[str]) -> Set[str]:
    with resource_stream(STOPWORDS_PACKAGE, STOPWORDS_PATH) as stream:
        stopwords = stream.read().decode().split()

    tokens_norm = set()
    for token in tokens_:
        token_norm = _normalize_text(token)
        if token_norm not in stopwords:
            tokens_norm.add(token_norm)
    return tokens_norm


@add_common_stats
def text_stats(series: pd.Series) -> Dict[str, Any]:
    """
    Compute summary statistics of a text feature.

    :param series: The feature to describe.
    :return: Descriptive statistics.
    """
    series = series.dropna()
    vocab = {token for doc in series for token in doc.split()}
    vocab_lower = {token.lower() for token in vocab}
    vocab_norm = _drop_stops_and_normalize(vocab)

    doc_lengths = series.str.len()

    stats = {
        'type': 'Text',
        'vocab_size': len(vocab),
        'vocab_size_lowercase': len(vocab_lower),
        'vocab_size_normalized': len(vocab_norm),
        'doc_length_min': np.nanmin(doc_lengths),
        'doc_length_median': np.nanmedian(doc_lengths),
        'doc_length_max': np.nanmax(doc_lengths),
        'doc_length_std': np.round(np.nanstd(doc_lengths), 4)
    }
    return stats


@add_common_stats
def numeric_stats(series: pd.Series) -> Dict[str, Any]:
    """
    Compute summary statistics of a numerical variable.

    :param series: The variable to describe.
    :return: Descriptive statistics.
    """
    stats = {
        'type': 'Numeric',
        'mean': series.mean(),
        'std': series.std(),
        'variance': series.var(),
        'min': series.min(),
        'max': series.max(),
        'kurtosis': series.kurt(),
        'skewness': series.skew(),
        'sum': series.sum(),
        'mean_abs_dev': series.mad(),
        'n_zeros': (series.shape[0] - np.count_nonzero(series)),
    }
    stats.update({"{:.0%}".format(percentile): series.dropna().quantile(percentile)
                  for percentile in [0.05, 0.25, 0.5, 0.75, 0.95]})
    stats['range'] = stats['max'] - stats['min']
    stats['iqr'] = stats['75%'] - stats['25%']
    stats['coef_of_var'] = stats['std'] / stats['mean'] if stats['mean'] else np.NaN
    stats['p_zeros'] = stats['n_zeros'] / series.shape[0]

    # round the result
    for key in stats.keys():
        try:
            stats[key] = round(stats[key], 4)
        except TypeError:
            pass

    return stats


@add_common_stats
def date_stats(series: pd.Series) -> Dict[str, Any]:
    """
    Compute summary statistics of a date variable.

    :param series: The variable to describe.
    :return: Descriptive statistics.
    """
    stats = {
        'type': 'Date',
        'min': series.min(),
        'max': series.max(),
    }
    stats['range'] = stats['max'] - stats['min']
    return stats


@add_common_stats
def categorical_stats(series: pd.Series) -> Dict[str, Any]:
    """
    Compute summary statistics of a categorical variable.

    :param series: The variable to describe.
    :return: Descriptive statistics.
    """
    stats = {
        'type': 'Categorical',
        'mode': series.mode()[0],
        'mode_freq': series.value_counts().max() / series.shape[0],
    }
    return stats


@add_common_stats
def constant_stats(series: pd.Series) -> Dict[str, Any]:
    """
    Compute summary statistics of a constant variable.

    :param series: The variable to describe.
    :return: Descriptive statistics.
    """
    stats = {'type': 'Constant'}
    return stats


@add_common_stats
def unique_stats(series: pd.Series) -> Dict[str, Any]:
    """
    Compute summary statistics of a unique variable.

    :param series: The variable to describe.
    :return: Descriptive statistics.
    """
    stats = {'type': 'Unique'}
    return stats

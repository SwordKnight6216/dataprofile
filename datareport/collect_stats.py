"""Collect the statistics for each variable in the dataset."""

from collections import defaultdict
from typing import List, Dict

import pandas as pd
from pandas.api.types import is_numeric_dtype

from datareport.config import DEFAULT_SAMPLE_SIZE, RANDOM_STATE
from .var_statistics import binary_stats, categorical_stats, constant_stats, datetime_stats, empty_stats, numeric_stats, \
    unique_stats


def get_variable_stats(df: pd.DataFrame) -> Dict[str, List[pd.Series]]:
    """
    Collect statistics from each variable.

    :param df: the target dataset
    :return: a dictionary contains statistics of all variables
    """
    var_stats = defaultdict(list)

    for col in df:

        distinct_count = df[col].nunique()
        leng = len(df[col])

        if distinct_count == 0:
            var_stats['Empty'].append(empty_stats(df[col]))
        elif distinct_count == 1:
            var_stats['Constant'].append(constant_stats(df[col]))
        elif distinct_count == 2:
            var_stats['Binary'].append(binary_stats(df[col]))
        elif pd.api.types.is_numeric_dtype(df[col]):
            var_stats['Numeric'].append(numeric_stats(df[col]))
        elif pd.api.types.is_datetime64_dtype(df[col]):
            var_stats['Date'].append(datetime_stats(df[col]))
        elif distinct_count == leng:
            var_stats['Unique'].append(unique_stats(df[col]))
        else:
            try:
                converted = pd.to_datetime(df[col])
                var_stats['Date'].append(datetime_stats(converted))
            except:
                var_stats['Categorical'].append(categorical_stats(df[col]))

    return var_stats


def get_table_stats(df: pd.DataFrame, var_stats: Dict[str, List[pd.Series]]) -> Dict[str, int]:
    """
    Extract information from the target dataset.

    :param df: the target dataset
    :param var_stats: statistics from each variable
    :return: a dictionary contains statistics of the target dataset
    """

    table_stats = {}
    table_stats['n_row'] = df.shape[0]
    table_stats['n_col'] = df.shape[1]
    table_stats['n_missing_cell'] = df.isnull().sum().sum()
    table_stats['n_duplicated_row'] = df.duplicated().sum()
    table_stats.update({'n_{}_var'.format(key): len(item) for key, item in var_stats.items()})

    return table_stats


def get_a_sample(df: pd.DataFrame, sample_size: int = DEFAULT_SAMPLE_SIZE,
                 random_state: int = RANDOM_STATE, file: str = None, line_ending: str = '\n') -> pd.DataFrame:
    """
    Provide the original dataset or a random sample of it.

    :param line_ending:
    :param file:
    :param df: the target dataset
    :param sample_size: Number of rows to sample from the target dataframe
    :param random_state: Random seed for the row sampler
    :return: the original dataset or a sample of it
    """
    try:
        sample_df = df.sample(sample_size, random_state=random_state)
        print(
            f'\nATTN: The following statistics are based on a {sample_size} sample out of {df.shape[0]} in the population. ',
            file=file, end=line_ending)

    except ValueError:
        print(
            f"\nSample size {sample_size} is larger than the population size {df.shape[0]}. using population instead.",
            file=file, end=line_ending)
        sample_df = df

    return sample_df


def get_data_type(df: pd.DataFrame, sample_size: int = DEFAULT_SAMPLE_SIZE,
                  random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """
    Provide a summary table of data types of the given dataset.

    :param df: the target dataset
    :param sample_size: Number of rows to sample from the target dataframe
    :param random_state: Random seed for the row sampler
    :return: a summary table of data types of the given dataset
    """
    sample_df = get_a_sample(df, sample_size, random_state)
    var_stats = get_variable_stats(sample_df)

    type_stats = ['type', 'count', 'n_missing', 'p_missing', 'n_unique', 'p_unique']
    tmp_df_stats = []
    for key, item in var_stats.items():
        tmp_df_stats.append(pd.DataFrame(item)[type_stats])

    return pd.concat(tmp_df_stats)

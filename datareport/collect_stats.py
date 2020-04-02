"""Collect the statistics for each variable in the dataset."""

from collections import defaultdict
from typing import List, Dict

import pandas as pd
from pandas.api.types import is_numeric_dtype

from datareport.config import DEFAULT_SAMPLE_SIZE, RANDOM_STATE
from .var_statistics import binary_stats, categorical_stats, constant_stats, datetime_stats, empty_stats, \
    numerical_stats, \
    unique_stats


def _get_actual_dtype(series:pd.Series) -> str:
    """

    :param series:
    :return: the name of actual data type in the given series
    """
    if pd.api.types.is_numeric_dtype(series):
        return 'Numerical'
    elif pd.api.types.is_bool_dtype(series):
        return 'Boolean'
    else:
        return 'Categorical'


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
            dty_empty = empty_stats(df[col])
            dty_empty['type'] = 'Useless'
            var_stats['Useless'].append(dty_empty)

        elif distinct_count == 1:
            dty_constant = constant_stats(df[col])
            dty_constant['type'] = 'Useless'
            var_stats['Useless'].append(dty_constant)

        elif distinct_count == leng:
            dty_unique = unique_stats(df[col])
            dty_unique['type'] = 'Useless'
            var_stats['Useless'].append(dty_unique)

        elif distinct_count == 2:
            dty_binary = binary_stats(df[col])
            dty_binary['type'] = 'Binary'
            dty_binary['data_type'] = _get_actual_dtype(df[col])
            var_stats['Binary'].append(dty_binary)

        elif pd.api.types.is_numeric_dtype(df[col]):
            dty_numerical = numerical_stats(df[col])
            dty_numerical['type'] = 'Interval'
            var_stats['Interval'].append(dty_numerical)

        elif pd.api.types.is_datetime64_dtype(df[col]):
            dty_datetime = datetime_stats(df[col])
            dty_datetime['type'] = 'Datetime'
            var_stats['Datetime'].append(dty_datetime)

        else:
            try:
                converted = pd.to_datetime(df[col])
                dty_datetime = datetime_stats(converted)
                dty_datetime['type'] = 'Datetime'
                dty_datetime['data_type'] = _get_actual_dtype(df[col])
                var_stats['Datetime'].append(dty_datetime)
            except:
                dty_categorical = categorical_stats(df[col])
                dty_categorical['type'] = 'Nominal'
                var_stats['Nominal'].append(dty_categorical)

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

    type_stats = ['type', 'data_type', 'count', 'n_missing', 'p_missing', 'n_unique', 'p_unique']
    tmp_df_stats = []
    for key, item in var_stats.items():
        tmp_df_stats.append(pd.DataFrame(item)[type_stats])

    return pd.concat(tmp_df_stats)

"""Collect the statistics for each variable in the dataset."""

from typing import List, Dict

import pandas as pd
from pandas.api.types import is_numeric_dtype, is_bool_dtype

from config import DEFAULT_SAMPLE_SIZE, RANDOM_STATE
from .var_statistics import boolean_stats
from .var_statistics import categorical_stats
from .var_statistics import constant_stats
from .var_statistics import date_stats
from .var_statistics import numeric_stats
from .var_statistics import unique_stats


def get_variable_stats(df: pd.DataFrame) -> Dict[str, List[pd.Series]]:
    """
    Collect statistics from each variable.

    :param df: the target dataset
    :return: a dictionary contains statistics of all variables
    """
    var_stats = {}

    col_with_no_values = []
    constant_stats_ls = []
    boolean_stats_ls = []
    numeric_stats_ls = []
    date_stats_ls = []
    unique_stats_ls = []
    categorical_stats_ls = []

    for col in df:

        distinct_count = df[col].nunique()
        leng = len(df[col])

        if distinct_count == 0:
            col_with_no_values.append(col)

        elif distinct_count == 1:
            constant_stats_ls.append(constant_stats(df[col]))
            var_stats['Constant'] = constant_stats_ls

        elif is_bool_dtype(df[col]) or (distinct_count == 2 and is_numeric_dtype(df[col]) and df[col].max() == 1):
            boolean_stats_ls.append(boolean_stats(df[col]))
            var_stats['Boolean'] = boolean_stats_ls

        elif pd.api.types.is_numeric_dtype(df[col]):
            numeric_stats_ls.append(numeric_stats(df[col]))
            var_stats['Numeric'] = numeric_stats_ls

        elif pd.api.types.is_datetime64_dtype(df[col]):
            date_stats_ls.append(date_stats(df[col]))
            var_stats['Date'] = date_stats_ls

        elif distinct_count == leng:
            unique_stats_ls.append(unique_stats(df[col]))
            var_stats['Unique'] = unique_stats_ls

        else:
            categorical_stats_ls.append(categorical_stats(df[col]))
            var_stats['Categorical'] = categorical_stats_ls

    if col_with_no_values:
        print(f'ATTN: Completely empty variables {col_with_no_values} are skipped in statistical calculation.')

    return var_stats


def get_table_stats(df: pd.DataFrame, var_stats: Dict[str, List[pd.Series]]) -> Dict[str, int]:
    """
    Extract information from the target dataset.

    :param df: the target dataset
    :param var_stats: statistics from each variable
    :return: a dictionary contains statistics of the target dataset
    """
    var_stats = var_stats

    table_stats = {}
    table_stats['n_row'] = df.shape[0]
    table_stats['n_col'] = df.shape[1]
    table_stats['n_missing'] = df.isnull().sum().sum()
    table_stats['n_duplicated'] = df.duplicated().sum()
    table_stats.update({'n_{}'.format(key): len(item) for key, item in var_stats.items()})

    return table_stats


def get_a_sample(df: pd.DataFrame, sample_size: int = DEFAULT_SAMPLE_SIZE,
                 random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """
    Provide the original dataset or a random sample of it.

    :param df: the target dataset
    :param sample_size: Number of rows to sample from the target dataframe
    :param random_state: Random seed for the row sampler
    :return: the original dataset or a sample of it
    """
    if sample_size < df.shape[0]:
        sample_df = df.sample(sample_size, random_state=random_state)
        print(f'ATTN: The following calculation are based on a {sample_size} sample. \n')
        return sample_df
    else:
        return df


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

    type_stats = ['type', 'count', 'distinct_count', 'p_missing', 'n_missing', 'p_unique', 'is_unique']
    tmp_df_stats = []
    for key, item in var_stats.items():
        tmp_df_stats.append(pd.DataFrame(item)[type_stats])

    return pd.concat(tmp_df_stats)

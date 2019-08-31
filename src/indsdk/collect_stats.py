"""Collect the statistics for each variable in the dataset."""
import logging
from collections import defaultdict
from typing import List, Dict, DefaultDict

import pandas as pd

from dsdk.data_report.var_statistics import DataType, get_stats_fn_by_type, common_stats
from dsdk.feature_types import infer_feature_type

logger = logging.getLogger(__name__)


def get_variable_stats(df: pd.DataFrame) -> Dict[DataType, List[pd.Series]]:
    """
    Collect statistics from each variable.

    :param df: the target dataset
    :return: a dictionary contains statistics of all variables
    """
    var_stats: DefaultDict[DataType, List[pd.Series]] = defaultdict(list)

    empty_cols: List[str] = []

    for col_ixd, col in enumerate(df.columns):
        data_type = infer_feature_type(df[col])

        if data_type == DataType.EMPTY:
            empty_cols.append(col)
            stats = common_stats(df[col])
            stats['type'] = 'Empty'
        else:
            stats_fn = get_stats_fn_by_type(data_type)
            stats = stats_fn(df[col])
        stats['feature_position'] = col_ixd
        var_stats[data_type].append(stats)

    if empty_cols:
        logger.info(f'ATTN: Completely empty variables {empty_cols} are skipped in statistical calculation.')

    return dict(var_stats)


def get_table_stats(df: pd.DataFrame, var_stats: Dict[DataType, List[pd.Series]]) -> Dict[str, int]:
    """
    Extract information from the target dataset.

    :param df: the target dataset
    :param var_stats: statistics from each variable
    :return: a dictionary contains statistics of the target dataset
    """
    table_stats = dict()
    table_stats['n_row'] = df.shape[0]
    table_stats['n_col'] = df.shape[1]
    table_stats['n_missing'] = df.isnull().sum().sum()
    table_stats['n_duplicated'] = df.duplicated().sum()
    table_stats.update({f'n_{str(key).split(".")[-1].lower()}': len(item) for key, item in var_stats.items()})

    return table_stats


def get_a_sample(df: pd.DataFrame, sample_size: int = 15000, random_state: int = 0) -> pd.DataFrame:
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


def get_data_type(df: pd.DataFrame, sample_size: int = 15000, random_state: int = 0) -> pd.DataFrame:
    """
    Provide a summary table of data types of the given dataset.

    :param df: the target dataset
    :param sample_size: Number of rows to sample from the target dataframe
    :param random_state: Random seed for the row sampler
    :return: a summary table of data types of the given dataset
    """
    sample_df = get_a_sample(df, sample_size, random_state)
    var_stats = get_variable_stats(sample_df)

    type_stats = ['feature_position', 'type', 'count', 'distinct_count', 'p_missing', 'n_missing',
                  'p_unique', 'is_unique']
    tmp_df_stats = []
    for key, item in var_stats.items():
        tmp_df_stats.append(pd.DataFrame(item)[type_stats])
    report = pd.concat(tmp_df_stats).sort_values(by='feature_position')

    return report

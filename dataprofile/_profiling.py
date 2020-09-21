"""Collect the statistics for each variable in the dataset."""

import datetime
import multiprocessing
from collections import defaultdict
from functools import wraps
from itertools import combinations
from typing import List, Dict, Union, Tuple, Callable, Any

import numpy
import pandas as pd
import tqdm
from loguru import logger

from ._config import DEFAULT_SAMPLE_SIZE, RANDOM_STATE, MAX_STRING_SIZE
from ._var_statistics import binary_stats, categorical_stats, datetime_stats, numerical_stats, base_stats


def _get_actual_dtype(series: pd.Series) -> str:
    """

    :param series:
    :return: the name of actual data type in the given series
    """
    if pd.api.types.is_bool_dtype(series):
        return 'Boolean'
    elif pd.api.types.is_numeric_dtype(series):
        return 'Numerical'
    else:
        return 'Categorical'


def _format_value(v: Any, max_size: int = MAX_STRING_SIZE) -> str:
    """
    Convert any input value to an appropriate str output

    :param v: input value
    :param max_size: max number of chars to display
    :return: changed string
    """

    if isinstance(v, bool):
        return str(v)
    if isinstance(v, numpy.int64) or isinstance(v, int):
        return f"{v:,d}"
    elif isinstance(v, numpy.float64) or isinstance(v, float):
        return f"{v:,.4f}"
    elif isinstance(v, str) and len(v) > max_size:
        return f"{v[:max_size]}..."
    return v


def _format_series(series: pd.Series) -> pd.Series:
    """
    change the output format for different value type.

    :param series: target series
    :return:
    """

    return series.apply(_format_value)


def _format_series_decor(original_func: Callable) -> Callable:
    """
    change the output format for different value type.

    :param original_func: target function to wrap
    :return:
    """

    @wraps(original_func)
    def wrapped_func(*args, **kwargs):
        type_, series = original_func(*args, **kwargs)
        return type_, series.apply(_format_value)

    return wrapped_func


@_format_series_decor
def _cal_var_stats(series: pd.Series) -> Tuple[str, pd.Series]:
    """
    used to classify variable types regarding machine learning.
    :param series: target series
    :return: valuable type and calculated statistics
    """

    distinct_count = series.nunique()
    leng = len(series)
    non_missing_cnt = series.count()

    if distinct_count == 0:
        dty_empty = base_stats(series)
        dty_empty['type'] = 'ZeroVar'
        dty_empty['data_type'] = 'Empty'
        return 'Useless', dty_empty

    elif distinct_count == 1 and leng == non_missing_cnt:
        dty_constant = base_stats(series)
        dty_constant['type'] = 'ZeroVar'
        dty_constant['data_type'] = 'Constant'
        return 'Useless', dty_constant

    elif distinct_count == leng and not pd.api.types.is_numeric_dtype(series):
        dty_unique = base_stats(series)
        dty_unique['type'] = 'Unique'
        dty_unique['data_type'] = 'Unique'
        return 'Useless', dty_unique

    elif distinct_count == 2 or (distinct_count == 1 and leng != non_missing_cnt):
        dty_binary = binary_stats(series)
        dty_binary['type'] = 'Binary'
        dty_binary['data_type'] = _get_actual_dtype(series)
        return 'Binary', dty_binary

    elif pd.api.types.is_numeric_dtype(series):
        dty_numerical = numerical_stats(series)
        dty_numerical['type'] = 'Interval'
        return 'Interval', dty_numerical

    elif pd.api.types.is_datetime64_dtype(series):
        dty_datetime = datetime_stats(series)
        dty_datetime['type'] = 'Datetime'
        return 'Datetime', dty_datetime

    else:
        try:
            converted = pd.to_datetime(series)
            dty_datetime = datetime_stats(pd.Series(converted))
            dty_datetime['type'] = 'Datetime'
            dty_datetime['data_type'] = _get_actual_dtype(series)
            return 'Datetime', dty_datetime
        except:
            dty_categorical = categorical_stats(series)
            dty_categorical['type'] = 'Nominal'
            return 'Nominal', dty_categorical


def get_variable_stats(df: pd.DataFrame, num_works: int = -1) -> Dict[str, List[pd.Series]]:
    """
    Collect types and statistics from each variable.

    :param df: the target dataset
    :param num_works: number of cpu cores for multiprocessing
    :return: a dictionary contains statistics of all variables
    """

    logger.info("Calculating statistics for each variable...")
    var_stats = defaultdict(list)
    num_works = multiprocessing.cpu_count() if num_works < 1 else num_works

    log_info_header = datetime.datetime.today().strftime("%Y-%m-%d at %X|INFO|")
    with multiprocessing.Pool(num_works) as executor:
        results = list(tqdm.tqdm(executor.imap_unordered(_cal_var_stats, (df[x] for x in df)), total=df.shape[1],
                                 desc=f"{log_info_header}Profiling variables",
                                 bar_format='{l_bar}{bar:40}{n_fmt}/{total_fmt}'))

    for k, v in results:
        var_stats[k].append(v)

    return var_stats


def get_table_stats(df: pd.DataFrame, var_stats: Dict[str, List[pd.Series]]) -> pd.DataFrame:
    """
    Extract information from the target dataset.

    :param df: the target dataset
    :param var_stats: statistics from each variable
    :return: a dictionary contains statistics of the target dataset
    """

    logger.info(f"Getting 'Table Statistics' ready...")
    table_stats = {'n_row': df.shape[0],
                   'n_col': df.shape[1],
                   'n_missing_cell': df.isnull().sum().sum(),
                   'n_empty_row': df.shape[0] - df.dropna(how='all').shape[0],
                   'n_duplicated_row': df.duplicated().sum()}
    table_stats.update({'n_{}_var'.format(key): len(item) for key, item in var_stats.items()})

    return pd.DataFrame(_format_series(pd.Series(table_stats)), columns=['count'])


def get_var_summary(var_stats: Dict[str, List[pd.Series]]) -> pd.DataFrame:
    """
    Provide a summary table of data types of the given dataset.

    :param var_stats: already get variable statistics
    :return: a summary table of data types of the given dataset
    """

    logger.info("Getting 'Variable Summary' ready...")
    type_stats = ['type', 'data_type', 'count', 'n_missing', 'p_missing', 'n_unique', 'p_unique']
    tmp_df_stats = []
    for key, item in var_stats.items():
        tmp_df_stats.append(pd.DataFrame(item)[type_stats])

    return pd.concat(tmp_df_stats)


def get_confusion_matrix(df: pd.DataFrame, var_stats: Dict[str, List[pd.Series]]) -> List[pd.DataFrame]:
    """
    Provide confusion matrices for all combination of binary variables.

    :param df:
    :param var_stats:
    :return: a list of confusion matrices
    """

    logger.info("Getting 'Confusion Matrix' ready...")
    cm_lt = []
    binary_vars = [var.name for var in var_stats['Binary']]
    for a, b in combinations(binary_vars, 2):
        logger.debug(f"Calculating confusion matrix of {a} and {b}")
        confusion_matrix = pd.crosstab(df[a].astype(str), df[b].astype(str))
        cm_lt.append(confusion_matrix)
    return cm_lt


def get_a_sample(df: pd.DataFrame, sample_size: int = DEFAULT_SAMPLE_SIZE,
                 random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """
    Provide the original dataset or a random sample of it.

    :param df: the target dataset
    :param sample_size: Number of rows to sample from the target dataframe
    :param random_state: Random seed for the row sampler
    :return: the original dataset or a sample of it
    """
    try:
        sample_df = df.sample(sample_size, random_state=random_state)
        logger.info(f'ATTN: The following statistics are based on {sample_size} samples '
                    f'out of {df.shape[0]} of the population.')

    except ValueError:
        logger.warning(f"Sample size {sample_size} is larger than the population size {df.shape[0]}. "
                       f"using population instead.")
        sample_df = df

    return sample_df


def get_df_profile(df: pd.DataFrame, num_works: int = -1) \
        -> Dict[str, Union[pd.DataFrame, list, Dict[str, pd.DataFrame]]]:
    """
    Collect all type of statistics together into one dictionary.

    :param df:
    :param num_works:
    :return:
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("only pandas DataFrames can be profiled! ")

    logger.info("Collecting stats for data profile...")
    df_profile = {}
    var_stats = get_variable_stats(df, num_works)

    df_profile['table_stats'] = get_table_stats(df, var_stats)
    df_profile['var_summary'] = get_var_summary(var_stats)

    df_profile['var_stats'] = {}
    logger.info("Getting 'Variable Statistics' ready...")
    for key, item in var_stats.items():
        logger.debug(f"Extracting statistics for {key} variables...")
        df_profile[f'var_stats'][f'{key}'] = pd.DataFrame(item).drop(['data_type', 'type'], axis=1)

    if 'Binary' in var_stats and len([var.name for var in var_stats['Binary']]) > 1:
        df_profile['conf_matrix'] = get_confusion_matrix(df, var_stats)

    return df_profile

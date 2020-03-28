import os
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal

from datareport.var_statistics import common_stats
from datareport.var_statistics import boolean_stats
from datareport.var_statistics import numeric_stats
from datareport.var_statistics import date_stats
from datareport.var_statistics import unique_stats
from datareport.var_statistics import constant_stats
from datareport.var_statistics import categorical_stats

TEST_FILE = '../../data/titanic/train.csv'
test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), TEST_FILE))


def test_common_stats():
    output = common_stats(test_df['Cabin'])
    expected_result = pd.Series({'count': 891,
                                 'distinct_count': 147,
                                 'p_missing': 0.771,
                                 'n_missing': 687,
                                 'is_unique': False,
                                 'p_unique': 0.7206})
    expected_result.name = 'Cabin'
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_boolean_stats():
    test_series = pd.Series([None, False, np.nan, True, False, True])
    output = boolean_stats(test_series)
    expected_result = pd.Series({'count': 6,
                                 'distinct_count': 3,
                                 'p_missing': 0.3333,
                                 'n_missing': 2,
                                 'is_unique': False,
                                 'p_unique': 0.75,
                                 'type': 'Boolean',
                                 'mode': False,
                                 'mode_freq': 2,
                                 'mean': 0.5})
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_numeric_stats():
    output = numeric_stats(test_df['Age'])
    expected_result = pd.Series({'count': 891,
                                 'distinct_count': 88,
                                 'p_missing': 0.1987,
                                 'n_missing': 177,
                                 'is_unique': False,
                                 'p_unique': 0.1232,
                                 'type': 'Numeric',
                                 'mean': 29.6991,
                                 'std': 14.5265,
                                 'variance': 211.0191,
                                 'min': 0.42,
                                 'max': 80.0,
                                 'range': 79.58,
                                 '5%': 4.0,
                                 '25%': 20.125,
                                 '50%': 28.0,
                                 '75%': 38.0,
                                 '95%': 56.0,
                                 'iqr': 17.875,
                                 'kurtosis': 0.1783,
                                 'skewness': 0.3891,
                                 'sum': 21205.17,
                                 'mean_abs_dev': 11.3229,
                                 'coff_of_var': 0.4891,
                                 'n_zeros': 0,
                                 'p_zeros': 0.0})
    expected_result.name = 'Age'
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_date_stats():
    test_series = pd.to_datetime(pd.Series(['9/16/2018',
                                            '8/30/2018',
                                            '7/29/2018',
                                            '',
                                            None,
                                            np.nan,
                                            '8/30/2018',
                                            '7/29/2018',
                                            '10/1/2018']))
    output = date_stats(test_series)
    expected_result = pd.Series({'count': 9,
                                 'distinct_count': 4,
                                 'p_missing': 0.3333,
                                 'n_missing': 3,
                                 'is_unique': False,
                                 'p_unique': 0.6667,
                                 'type': 'Date',
                                 'min': pd.to_datetime('2018-07-29 00:00:00'),
                                 'max': pd.to_datetime('2018-10-01 00:00:00'),
                                 'range': pd.to_timedelta('64 days 00:00:00')})
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_constant_stats():
    test_series = pd.Series([1, 1, np.nan, 1, None, 1, 1, 1, 1])
    output = constant_stats(test_series)
    expected_result = pd.Series({'count': 9,
                                 'distinct_count': 1,
                                 'p_missing': 0.2222,
                                 'n_missing': 2,
                                 'is_unique': False,
                                 'p_unique': 0.1429,
                                 'type': 'Constant'})
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_unique_stats():
    output = unique_stats(test_df['Name'])
    expected_result = pd.Series({'count': 891,
                                 'distinct_count': 891,
                                 'p_missing': 0.0,
                                 'n_missing': 0,
                                 'is_unique': True,
                                 'p_unique': 1.0,
                                 'type': 'Unique'})
    expected_result.name = 'Name'
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_categorical_stats():
    output = categorical_stats(test_df['Embarked'])
    expected_result = pd.Series({'count': 891,
                                 'distinct_count': 3,
                                 'p_missing': 0.0022,
                                 'n_missing': 2,
                                 'is_unique': False,
                                 'p_unique': 0.0034,
                                 'type': 'Categorical',
                                 'mode': 'S',
                                 'mode_freq': 644})
    expected_result.name = 'Embarked'
    assert_series_equal(output.sort_index(), expected_result.sort_index())

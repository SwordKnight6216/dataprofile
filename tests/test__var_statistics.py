import os

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal

from dataprofile._var_statistics import base_stats
from dataprofile._var_statistics import binary_stats
from dataprofile._var_statistics import categorical_stats
from dataprofile._var_statistics import datetime_stats
from dataprofile._var_statistics import numerical_stats


@pytest.fixture()
def test_df():
    test_file = '../data/titanic/train.csv'
    test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), test_file))
    return test_df


def test_base_stats(test_df):
    output = base_stats(test_df['Cabin'])
    expected_result = pd.Series({'count': 891,
                                 'n_unique': 147,
                                 'p_missing': '77.10%',
                                 'n_missing': 687,
                                 'p_unique': '72.06%'})
    expected_result.name = 'Cabin'
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_binary_stats():
    series = pd.Series([True, False, True, False, True], name='test')
    result = binary_stats(series)
    
    expected_stats = {
        'count': 5,
        'n_missing': 0,
        'p_missing': '0.00%',
        'n_unique': 2,
        'p_unique': '40.00%',
        'data_type': 'Binary',
        'value1': 'True',
        'n_value1': 3,
        'p_value1': '60.00%',
        'value2': 'False',
        'n_value2': 2,
        'p_value2': '40.00%'
    }
    
    pd.testing.assert_series_equal(result, pd.Series(expected_stats, name='test'))


def test_numerical_stats():
    series = pd.Series([1, 2, 3, 4, 5], name='test')
    result = numerical_stats(series)
    
    expected_stats = {
        'count': 5,
        'n_missing': 0,
        'p_missing': '0.00%',
        'n_unique': 5,
        'p_unique': '100.00%',
        'data_type': 'Numerical',
        'mean': 3.0,
        'std': series.std(),
        'variance': series.var(),
        'min': 1,
        'max': 5,
        'range': 4,
        'mean_abs_dev': (series - series.mean()).abs().mean(),
        # Add other expected values
    }
    
    for key, value in expected_stats.items():
        assert result[key] == value


def test_datetime_stats():
    test_series = pd.to_datetime(pd.Series(['9/16/2018',
                                            '8/30/2018',
                                            '7/29/2018',
                                            '',
                                            None,
                                            np.nan,
                                            '8/30/2018',
                                            '7/29/2018',
                                            '10/1/2018']))
    output = datetime_stats(test_series)
    expected_result = pd.Series({'count': 9,
                                 'n_unique': 4,
                                 'p_missing': '33.33%',
                                 'n_missing': 3,
                                 'p_unique': '66.67%',
                                 'data_type': 'Datetime',
                                 'min': pd.to_datetime('2018-07-29 00:00:00'),
                                 '5%': pd.to_datetime('2018-07-29 00:00:00'),
                                 '25%': pd.to_datetime('2018-08-06 00:00:00'),
                                 '50%': pd.to_datetime('2018-08-30 00:00:00'),
                                 '75%': pd.to_datetime('2018-09-11 18:00:00'),
                                 '95%': pd.to_datetime('2018-09-27 06:00:00'),
                                 'max': pd.to_datetime('2018-10-01 00:00:00'),
                                 'range': pd.to_timedelta('64 days 00:00:00'),
                                 'n_Monday': 1,
                                 'n_Tuesday': 0,
                                 'n_Wednesday': 0,
                                 'n_Thursday': 2,
                                 'n_Friday': 0,
                                 'n_Saturday': 0,
                                 'n_Sunday': 3})
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_constant_stats():
    test_series = pd.Series([1, 1, np.nan, 1, None, 1, 1, 1, 1])
    output = base_stats(test_series)
    expected_result = pd.Series({'count': 9,
                                 'n_unique': 1,
                                 'p_missing': '22.22%',
                                 'n_missing': 2,
                                 'p_unique': '14.29%', })
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_unique_stats(test_df):
    output = base_stats(test_df['Name'])
    expected_result = pd.Series({'count': 891,
                                 'n_unique': 891,
                                 'p_missing': '0.00%',
                                 'n_missing': 0,
                                 'p_unique': '100.00%', })
    expected_result.name = 'Name'
    assert_series_equal(output.sort_index(), expected_result.sort_index())


def test_categorical_stats(test_df):
    output = categorical_stats(test_df['Embarked'])
    expected_result = pd.Series({'count': 891,
                                 'n_unique': 3,
                                 'p_missing': '0.22%',
                                 'n_missing': 2,
                                 'p_unique': '0.34%',
                                 'data_type': 'Categorical',
                                 'mode': 'S',
                                 'mode_freq': 644,
                                 '2nd_freq_value': 'C',
                                 '2nd_freq': 168,
                                 '3rd_freq_value': 'Q',
                                 '3rd_freq': 77})
    expected_result.name = 'Embarked'
    assert_series_equal(output.sort_index(), expected_result.sort_index())

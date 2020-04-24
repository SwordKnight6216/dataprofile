import os

import pandas as pd
import pytest

from .._profiling import _get_actual_dtype, _format_value, _cal_var_stats
from .._profiling import get_a_sample, get_df_profile, get_table_stats, get_var_summary, get_variable_stats


@pytest.fixture()
def test_df():
    test_file = '../../data/titanic/train.csv'
    test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), test_file))
    test_df['no_values'] = None
    return test_df


@pytest.mark.parametrize("test_input, expected",
                         [(pd.Series([1, 2, 3, 4, 5]), 'Numerical'),
                          (pd.Series([True, False, False]), 'Boolean'),
                          (pd.Series([1, 0, 0, 0, 1, None]), 'Numerical'),
                          (pd.Series([True, 'False', 18]), 'Categorical')])
def test__get_actual_dtype(test_input, expected):
    assert _get_actual_dtype(test_input) == expected


@pytest.mark.parametrize("test_input, max_size, expected",
                         [(True, 10, 'True'), (3, 5, '3'), (1.23456, 6, '1.2346'), ('abcd', 3, 'abc...')])
def test__format_value(test_input, max_size, expected):
    assert _format_value(test_input, max_size) == expected


def test_get_variable_stats(test_df):
    var_stats = get_variable_stats(test_df)
    assert set(var_stats.keys()) == {'Interval', 'Binary', 'Useless', 'Nominal'}
    # check some statistics randomly
    assert len(var_stats['Interval']) == 5
    assert len(var_stats['Binary']) == 2
    assert len(var_stats['Nominal']) == 3
    assert len(var_stats['Useless']) == 3
    assert pd.api.types.is_numeric_dtype(test_df[var_stats['Interval'][1].name])


def test_get_table_stats(test_df):
    table_stats = get_table_stats(test_df, get_variable_stats(test_df))['count'].to_dict()
    expected_result = {'n_row': '891',
                       'n_col': '13',
                       'n_missing_cell': '1,757',
                       'n_empty_row': '0',
                       'n_duplicated_row': '0',
                       'n_Interval_var': '5',
                       'n_Binary_var': '2',
                       'n_Useless_var': '3',
                       'n_Nominal_var': '3', }
    print(table_stats)
    assert table_stats == expected_result


def test_get_a_sample(test_df):
    sample = get_a_sample(test_df, 100, 2018)
    assert sample.shape == (100, 13)
    assert sample.iloc[10, 5] == 21


def test_get_a_sample_exception(test_df):
    # with pytest.raises(ValueError):
    sample = get_a_sample(test_df, test_df.shape[0] + 10, 2018)
    assert sample.shape == test_df.shape


def test_get_data_type(test_df):
    data_type = get_var_summary(get_variable_stats(df=test_df))
    expected_result = {'PassengerId': 'Unique',
                       'Pclass': 'Numerical',
                       'Age': 'Numerical',
                       'SibSp': 'Numerical',
                       'Parch': 'Numerical',
                       'Fare': 'Numerical',
                       'Survived': 'Numerical',
                       'Name': 'Unique',
                       'Sex': 'Categorical',
                       'Ticket': 'Categorical',
                       'Cabin': 'Categorical',
                       'Embarked': 'Categorical',
                       'no_values': 'Empty'}
    assert dict(data_type['data_type']) == expected_result


def test_get_df_profile_type_error():
    with pytest.raises(TypeError):
        get_df_profile('test')


def test_get_df_profile(test_df):
    result = get_df_profile(test_df)
    assert 'table_stats' in result
    assert 'var_summary' in result
    assert 'var_stats' in result


@pytest.mark.parametrize("test_input, expected",
                         [(pd.Series([1, 2, 3, 4, 5]), 'Useless'),
                          (pd.Series([True, False, True, False, False]), 'Binary'),
                          (pd.Series([1, 0, 0, 0, 1, 1, 1, 0]), 'Binary'),
                          (pd.Series([True, 'False', 18]), 'Useless'),
                          (pd.Series(['True', 'False', 'True', 'False', '18']), 'Nominal')])
def test__cal_var_stats(test_input, expected):
    assert expected == _cal_var_stats(test_input)[0]

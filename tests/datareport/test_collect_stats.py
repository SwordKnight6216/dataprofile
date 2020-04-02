import pandas as pd
import os
from pandas.api.types import is_numeric_dtype

from datareport.collect_stats import get_variable_stats
from datareport.collect_stats import get_table_stats
from datareport.collect_stats import get_a_sample
from datareport.collect_stats import get_var_summary

TEST_FILE = '../../data/titanic/train.csv'
test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), TEST_FILE))
# add an empty column for testing purpose
test_df['no_values'] = None


def test_get_variable_stats():
    var_stats = get_variable_stats(test_df)
    assert set(var_stats.keys()) == set(['Interval', 'Binary', 'Useless', 'Nominal'])
    # check some statistics randomly
    assert len(var_stats['Interval']) == 5
    assert len(var_stats['Binary']) == 2
    assert len(var_stats['Nominal']) == 3
    assert len(var_stats['Useless']) == 3
    assert is_numeric_dtype(test_df[var_stats['Interval'][1].name])


def test_get_table_stats():
    table_stats = get_table_stats(test_df, get_variable_stats(test_df))
    expected_result = {'n_row': 891,
                       'n_col': 13,
                       'n_missing_cell': 1757,
                       'n_duplicated_row': 0,
                       'n_Interval_var': 5,
                       'n_Binary_var': 2,
                       'n_Useless_var': 3,
                       'n_Nominal_var': 3,}
    assert table_stats == expected_result


def test_get_a_sample():
    sample = get_a_sample(test_df, 100, 2018)
    assert sample.shape == (100, 13)
    assert sample.iloc[10, 5] == 21


def test_get_data_type():
    data_type = get_var_summary(df=test_df)
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

import pandas as pd
import os
from pandas.api.types import is_numeric_dtype

from datareport.collect_stats import get_variable_stats
from datareport.collect_stats import get_table_stats
from datareport.collect_stats import get_a_sample
from datareport.collect_stats import get_data_type

TEST_FILE = '../../data/titanic/train.csv'
test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), TEST_FILE))
# add an empty column for testing purpose
test_df['no_values'] = None


def test_get_variable_stats():
    var_stats = get_variable_stats(test_df)
    assert list(var_stats.keys()) == ['Numeric', 'Boolean', 'Unique', 'Categorical']
    # check some statistics randomly
    assert len(var_stats['Numeric']) == 6
    assert len(var_stats['Boolean']) == 1
    assert len(var_stats['Unique']) == 1
    assert len(var_stats['Categorical']) == 4
    assert is_numeric_dtype(test_df[var_stats['Numeric'][1].name])


def test_get_table_stats():
    table_stats = get_table_stats(test_df, get_variable_stats(test_df))
    expected_result = {'n_row': 891,
                       'n_col': 13,
                       'n_missing': 1757,
                       'n_duplicated': 0,
                       'n_Numeric': 6,
                       'n_Boolean': 1,
                       'n_Unique': 1,
                       'n_Categorical': 4}
    assert table_stats == expected_result


def test_get_a_sample():
    sample = get_a_sample(test_df, 100, 2018)
    assert sample.shape == (100, 13)
    assert sample.iloc[10, 5] == 21


def test_get_data_type():
    data_type = get_data_type(test_df)
    expected_result = {'PassengerId': 'Numeric',
                       'Pclass': 'Numeric',
                       'Age': 'Numeric',
                       'SibSp': 'Numeric',
                       'Parch': 'Numeric',
                       'Fare': 'Numeric',
                       'Survived': 'Boolean',
                       'Name': 'Unique',
                       'Sex': 'Categorical',
                       'Ticket': 'Categorical',
                       'Cabin': 'Categorical',
                       'Embarked': 'Categorical'}
    assert dict(data_type['type']) == expected_result

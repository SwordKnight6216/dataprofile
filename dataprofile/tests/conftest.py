import os

import pandas as pd
import pytest


@pytest.fixture()
def test_df():
    test_file = '../../data/titanic/train.csv'
    test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), test_file))
    test_df['no_values'] = None
    return test_df

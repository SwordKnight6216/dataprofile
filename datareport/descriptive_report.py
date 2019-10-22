"""Class/Transformer for printing an overall report of statistics and plots for a given dataset."""

import pandas as pd
from tabulate import tabulate
from sklearn.base import BaseEstimator, TransformerMixin

from .collect_stats import get_variable_stats, get_table_stats, get_a_sample


class DataReport(BaseEstimator, TransformerMixin):
    """
    This class is designed to print reports of statistics and plots.

    And can be inserted as a middle step in sklearn pipeline.
    """

    def __init__(self) -> None:
        """Initialization."""

    def print_report(self,
                     df: pd.DataFrame,
                     prt_table_stats: bool = True,
                     prt_var_stats: bool = True,
                     sample_size: int = 15000,
                     var_per_row: int = 6,
                     random_state: int = 0) -> None:
        """
        Print out descriptive analysis report for a given dataset.

        :param df: the target dataset
        :param prt_table_stats: if print the table statistics
        :param prt_var_stats: if print the variables statistics
        :param prt_corr_stats: if print the correlation table
        :param prt_plots: if print plots
        :param sample_size: Number of rows to sample from the target dataframe
        :param var_per_row: number of columns of stats to print per row
        :param random_state: Random seed for the row sampler
        :return: None
        """
        sample_df = get_a_sample(df, sample_size, random_state)

        var_stats = get_variable_stats(sample_df)

        if prt_table_stats:
            table_stats = get_table_stats(sample_df, var_stats)
            print('\n=============Table Statistics ============== \n')
            print(tabulate(pd.DataFrame(pd.Series(table_stats), columns=['count']), headers='keys', tablefmt='psql'))

        if prt_var_stats:
            print('\n===============Variables Statistics ============ ')
            for key, item in var_stats.items():
                print(f'\nSummary of {key} variables: \n')
                for i in range(len(var_stats[key]) // var_per_row + 1):
                    print(tabulate(
                        pd.DataFrame(item).drop('type', axis=1).T.iloc[:, (i) * var_per_row:(i + 1) * var_per_row], \
                        headers='keys', tablefmt='psql'))

    def fit(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> pd.DataFrame:
        """
        Run the report and return the same dataset.

        :param X: the X of target dataset
        :param y: y
        :return: the original dataset
        """
        return X

    def transform(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> pd.DataFrame:
        """
        Run the report and return the same dataset.

        :param X: the X of target dataset
        :param y: y
        :return: the original dataset
        """
        self.print_report(X, **kwargs)
        return X

    def fit_transform(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> pd.DataFrame:
        """
        Run the report and return the same dataset.

        :param X: the X of target dataset
        :param y: y
        :return: the original datase
        """
        self.transform(self.fit(X, **kwargs), **kwargs)
        return X

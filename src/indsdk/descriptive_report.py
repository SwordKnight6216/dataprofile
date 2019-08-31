"""Class/Transformer for printing an overall report of statistics and plots for a given dataset."""
import logging

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from tabulate import tabulate

from dsdk.data_report.collect_stats import get_variable_stats, get_table_stats, get_a_sample
from dsdk.viz.feature_viz import create_corr_heatmap, plot_feature_distribution_df
from dsdk.viz.feature_viz import get_corr_df


class DataReport(BaseEstimator, TransformerMixin):
    """
    This class is designed to print reports of statistics and plots.

    And can be inserted as a middle step in sklearn pipeline.
    """

    def __init__(self) -> None:
        """Initialization."""
        pass

    def print_report(self,
                     df: pd.DataFrame,
                     prt_table_stats: bool = True,
                     prt_var_stats: bool = True,
                     prt_corr_stats: bool = False,
                     prt_plots: bool = False,
                     sample_size: int = 15000,
                     var_per_row: int = 6,
                     random_state: int = 0) -> None:
        """
        Print out descriptive analysis report for a given data set.

        :param df: the target data set.
        :param prt_table_stats: if print the table statistics.
        :param prt_var_stats: if print the variables statistics.
        :param prt_corr_stats: if print the correlation table.
        :param prt_plots: if print plots.
        :param sample_size: Number of rows to sample from the target DataFrame.
        :param var_per_row: number of columns of stats to print per row.
        :param random_state: Random seed for the row sampler.
        :return: None
        """
        sample_df = get_a_sample(df, sample_size, random_state)

        var_stats = get_variable_stats(sample_df)
        corr_stats = get_corr_df(sample_df)

        logging.getLogger(__name__).info('Start to print the descriptive report ...')

        if prt_table_stats:
            table_stats = get_table_stats(sample_df, var_stats)
            print(f'\n=============Table Statistics ============== \n')
            print(tabulate(pd.DataFrame(pd.Series(table_stats),
                                        columns=['count']), headers='keys', tablefmt='psql'))

        if prt_var_stats:
            print(f'\n===============Variables Statistics ============ ')
            for key, item in var_stats.items():
                print(f'\nSummary of {key} variables: \n')
                for i in range(len(var_stats[key]) // var_per_row + 1):
                    print(tabulate(
                        pd.DataFrame(item).drop('type', axis=1).T.iloc[:, (i) * var_per_row:(i + 1) * var_per_row],
                        headers='keys', tablefmt='psql'))

        if prt_corr_stats:
            print(f'\n===============Variables Correlations=========== \n')
            print(tabulate(corr_stats, headers='keys', tablefmt='psql'))

        if prt_plots:
            type_var = {key: [x.name for x in items] for key, items in var_stats.items()}
            print(f'\n===============Plots============================= \n')
            print(f'Variables Distributions: ')
            try:
                plot_feature_distribution_df(sample_df[type_var['Numeric']], [], [])
            except:
                logging.getLogger(__name__).warning('No numeric variables to print.')
            print(f'Correlation Heat map: ')
            create_corr_heatmap(corr_stats)

    # noinspection PyPep8Naming, PyUnusedLocal
    def fit(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> 'DataReport':
        """
        Run the report and return the same data set.

        :param X: the X of target data set.
        :param y: y.
        :return: the original data set.
        """
        return self

    # noinspection PyPep8Naming, PyUnusedLocal
    def transform(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> pd.DataFrame:
        """
        Run the report and return the same data set.

        :param X: the X of target data set.
        :param y: y.
        :return: the original data set.
        """
        self.print_report(X, **kwargs)
        return X

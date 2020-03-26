"""Class/Transformer for printing an overall report of statistics and plots for a given dataset."""

from pathlib import Path
from typing import Optional

import click
import pandas as pd
from tabulate import tabulate

# from sklearn.base import BaseEstimator, TransformerMixin
from config import DEFAULT_SAMPLE_SIZE
from datareport.collect_stats import get_variable_stats, get_table_stats, get_a_sample


def print_report(df: pd.DataFrame,
                 prt_table_stats: bool = True,
                 prt_var_stats: bool = True,
                 sample_size: int = DEFAULT_SAMPLE_SIZE,
                 var_per_row: int = 6,
                 random_state: int = 0,
                 report_file: str = '') -> None:
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
    :param report_file: store the report to a file
    :return: None
    """

    sample_df = get_a_sample(df, sample_size, random_state)

    var_stats = get_variable_stats(sample_df)

    if report_file:
        report_file = make_report_file(report_file)
        file = open(report_file, 'w', encoding="UTF-8")
    else:
        file = None

    try:
        if prt_table_stats:
            table_stats = get_table_stats(sample_df, var_stats)
            print('\n=============Table Statistics ============== \n', file=file)
            print(tabulate(pd.DataFrame(pd.Series(table_stats), columns=['count']), headers='keys', tablefmt='psql'),
                  file=file)

        if prt_var_stats:
            print('\n===============Variables Statistics ============ ', file=file)
            for key, item in var_stats.items():
                print(f'\nSummary of {key} variables: \n', file=file)
                for i in range(len(var_stats[key]) // (var_per_row + 1) + 1):
                    print(tabulate(
                        pd.DataFrame(item).drop('type', axis=1).T.iloc[:, (i) * var_per_row:(i + 1) * var_per_row], \
                        headers='keys', tablefmt='psql'), file=file)
    except:
        print('Report not finished successfully!')
    finally:
        file.close() if file else None


def make_report_file(file: str) -> Path:
    """
    create a file for store the report
    :param file:
    :return: created file
    """
    path = Path(file)
    if not path.exists():
        path.touch()
    return path


@click.command()
@click.option('--path', '-p', prompt='cvs file path', required=True, help='cvs format is required',
              default='/Users/gordonchen/Documents/projects/dataviz/data/raw/population/industry_sex_employment.csv',
              show_default=True)
@click.option('--prt_table_stats', prompt='print table statistics?', required=False, default=True, show_default=True,
              help='wanna see the overall dataset statistics')
@click.option('--prt_var_stats', prompt='print variable statistics?', required=False, default=True, show_default=True,
              help='wanna see the variable statistics')
@click.option('--sample_size', prompt='How big is your sample size?', required=False, default=DEFAULT_SAMPLE_SIZE,
              show_default=True,
              help='the size of sample in the analysis')
@click.option('--var_per_row', prompt='How many variables to show per row?', required=False, default=6,
              show_default=True,
              help='number of variables to show per row')
@click.option('--save_report_to_file', prompt='save report to a file', required=False, default='',
              show_default=True,
              help='save report to a file')
def main(path: str, prt_table_stats: bool = True,
         prt_var_stats: bool = True,
         sample_size: int = DEFAULT_SAMPLE_SIZE,
         var_per_row: int = 6, save_report_to_file: str = '') -> None:
    df = pd.read_csv(Path(path))
    #report_file = make_report_file(save_report_to_file) if save_report_to_file else ''
    print_report(df, prt_table_stats=prt_table_stats, prt_var_stats=prt_var_stats, sample_size=sample_size,
                 var_per_row=var_per_row, report_file=save_report_to_file)


if __name__ == "__main__":
    main()

# class DataReport(BaseEstimator, TransformerMixin):
#     """
#     This class is designed to print reports of statistics and plots.
#
#     And can be inserted as a middle step in sklearn pipeline.
#     """
#
#     def __init__(self) -> None:
#         """Initialization."""
#
#     def fit(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> pd.DataFrame:
#         """
#         Run the report and return the same dataset.
#
#         :param X: the X of target dataset
#         :param y: y
#         :return: the original dataset
#         """
#         return X
#
#     def transform(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> pd.DataFrame:
#         """
#         Run the report and return the same dataset.
#
#         :param X: the X of target dataset
#         :param y: y
#         :return: the original dataset
#         """
#         print_report(X, **kwargs)
#         return X
#
#     def fit_transform(self, X: pd.DataFrame, y: pd.Series = None, **kwargs) -> pd.DataFrame:
#         """
#         Run the report and return the same dataset.
#
#         :param X: the X of target dataset
#         :param y: y
#         :return: the original datase
#         """
#         self.transform(self.fit(X, **kwargs), **kwargs)
#         return X
